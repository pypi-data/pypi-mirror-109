import warnings
from typing import Dict, Optional

from gcip.core.job import Job


class Bootstrap(Job):
    def __init__(
        self,
        *,
        aws_account_id: str,
        aws_region: str,
        toolkit_stack_name: str,
        qualifier: str,
        job_name: str = "toolkit-stack",
        job_stage: str = "deploy",
        tags: Optional[Dict[str, str]] = None,
    ) -> None:
        script = [
            "cdk bootstrap",
            f"--toolkit-stack-name {toolkit_stack_name}",
            f"--qualifier {qualifier}",
            f"aws://{aws_account_id}/{aws_region}",
        ]

        if tags:
            script.extend([f"-t {k}={v}" for k, v in tags.items()])

        super().__init__(
            script=" ".join(script),
            name=job_name,
            stage=job_stage,
        )
        self.add_variables(CDK_NEW_BOOTSTRAP="1")


class Deploy(Job):
    def __init__(
        self,
        *stacks: str,
        toolkit_stack_name: str,
        strict: bool = True,
        wait_for_stack: bool = True,
        wait_for_stack_assume_role: Optional[str] = None,
        wait_for_stack_account_id: Optional[str] = None,
        deploy_options: Optional[str] = None,
        job_name: str = "cdk",
        job_stage: str = "deploy",
        context: Optional[Dict[str, str]] = None,
    ):
        stacks_string = " ".join(stacks)
        script = ["cdk deploy --require-approval 'never'"]

        if strict:
            script.append("--strict")

        if deploy_options:
            script.append(deploy_options)

        if context:
            script.extend([f"-c {k}={v}" for k, v in context.items()])

        script.append(f"--toolkit-stack-name {toolkit_stack_name}")
        script.append(stacks_string)

        super().__init__(
            name=job_name,
            stage=job_stage,
            script=" ".join(script),
        )

        if wait_for_stack:
            wait_for_stack_options = ""
            if wait_for_stack_assume_role:
                wait_for_stack_options += f" --assume-role {wait_for_stack_assume_role}"
                if wait_for_stack_account_id:
                    wait_for_stack_options += f" --assume-role-account-id {wait_for_stack_account_id}"
            elif wait_for_stack_account_id:
                warnings.warn("`wait_for_stack_account_id` has no effects without `wait_for_stack_assume_role`")

            self.prepend_scripts(
                "pip3 install gcip",
                f"python3 -m gcip.addons.aws.tools.wait_for_cloudformation_stack_ready --stack-names '{stacks_string}'{wait_for_stack_options}",
            )


class Diff(Job):
    def __init__(
        self,
        *stacks: str,
        job_name: str = "cdk",
        job_stage: str = "diff",
        diff_options: Optional[str] = None,
        context: Optional[Dict[str, str]] = None,
    ) -> None:
        script = ["cdk diff"]
        if diff_options:
            script.append(diff_options)

        if context:
            script.extend([f"-c {k}={v}" for k, v in context.items()])

        script.append(" ".join(stacks))
        super().__init__(
            name=job_name,
            stage=job_stage,
            script=" ".join(script),
        )
