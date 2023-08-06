from __future__ import annotations

import configparser
from dataclasses import dataclass
from getpass import getpass
from pathlib import Path
from typing import Optional, Dict, Final, Any

import boto3
import click
from dacite import from_dict

DEFAULT_AWS_CREDENTIALS_FILE_PATH: Final[Path] = Path.home() / ".aws/credentials"
DEFAULT_SESSION_DURATION_SECONDS: Final[int] = 14400
DEFAULT_SESSION_NAME: Final[str] = "YetAnotherSTSSession"


@dataclass()
class AWSProfile:
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    role_arn: Optional[str] = None
    source_profile: Optional[str] = None
    external_id: Optional[str] = None
    duration_seconds: Optional[str] = None
    mfa_serial: Optional[str] = None

    @property
    def contains_access_key(self) -> bool:
        return bool(self.aws_access_key_id and self.aws_secret_access_key)


@dataclass()
class AWSCredentialFile:
    profiles: Dict[str, AWSProfile]

    def get_profile(self, profile: str) -> Optional[AWSProfile]:
        return self.profiles.get(profile)

    @classmethod
    def from_config(cls, config: configparser.ConfigParser) -> AWSCredentialFile:
        return cls(
            profiles={
                profile: from_dict(data_class=AWSProfile, data=attributes) for profile, attributes in config.items()
            }
        )


def read_credentials_file(path: Optional[Path] = None) -> AWSCredentialFile:
    credentials_file_path = path or DEFAULT_AWS_CREDENTIALS_FILE_PATH
    config = configparser.ConfigParser()
    config.read(credentials_file_path)
    return AWSCredentialFile.from_config(config)


def get_source_profile(profile: AWSProfile, credentials_file: AWSCredentialFile) -> AWSProfile:
    if profile.source_profile:
        source_profile = credentials_file.get_profile(profile.source_profile)
        if not source_profile:
            raise ValueError(f"{profile.source_profile} source profile wasn't found in credentials file")
        return source_profile
    return profile


def update_credentials_file(response: Dict[str, Any], path: Optional[Path] = None) -> None:
    credentials_file_path = path or DEFAULT_AWS_CREDENTIALS_FILE_PATH
    config = configparser.ConfigParser()
    config.read(credentials_file_path)

    try:
        config.add_section("yaststool")
    except configparser.DuplicateSectionError:
        pass

    yaststool_config = config["yaststool"]
    yaststool_config["aws_access_key_id"] = response["Credentials"]["AccessKeyId"]
    yaststool_config["aws_secret_access_key"] = response["Credentials"]["SecretAccessKey"]
    yaststool_config["aws_session_token"] = response["Credentials"]["SessionToken"]

    with open(credentials_file_path, 'w') as credentials_file:
        config.write(credentials_file)


def assume_role(profile: AWSProfile, source_profile: AWSProfile) -> Dict[str, Any]:
    mfa_code = getpass(prompt="MFA Code: ") if profile.mfa_serial else None
    client = boto3.client(
        "sts",
        aws_access_key_id=source_profile.aws_access_key_id,
        aws_secret_access_key=source_profile.aws_secret_access_key,
    )

    duration_seconds = int(profile.duration_seconds) if profile.duration_seconds else DEFAULT_SESSION_DURATION_SECONDS
    kwargs = {"SerialNumber": profile.mfa_serial, "TokenCode": mfa_code} if mfa_code else {}
    response = client.assume_role(
        RoleArn=profile.role_arn,
        RoleSessionName=DEFAULT_SESSION_NAME,
        DurationSeconds=duration_seconds,
        **kwargs,
    )
    print(f"Role {profile.role_arn} successfully assumed")
    return response

@click.command()
@click.argument("profile_name")
def cli(profile_name: str) -> None:
    credentials_file = read_credentials_file()
    profile = credentials_file.get_profile(profile_name)
    if not profile:
        raise ValueError(f"{profile_name} profile wasn't found in credentials file")

    source_profile = get_source_profile(profile, credentials_file)
    response = assume_role(profile, source_profile)

    update_credentials_file(response)
    print("Updated yaststool profile in credentials file")

if __name__ == "__main__":
    cli()
