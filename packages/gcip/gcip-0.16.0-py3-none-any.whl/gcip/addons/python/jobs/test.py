from typing import Union, Optional

from gcip.lib import rules
from gcip.core.job import Job
from gcip.core.image import Image
from gcip.addons.python.scripts import (
    pip_install_requirements,
)
from gcip.addons.container.images import PredefinedImages


class Pytest(Job):
    def __init__(
        self,
        job_name: str = "pytest",
        job_stage: str = "test",
    ) -> None:
        """
        Runs `pytest` and installs project requirements before (`scripts.pip_install_requirements()`)

        * Requires a `requirements.txt` in your project folder containing at least `pytest`
        """
        super().__init__(
            name=job_name,
            stage=job_stage,
            script=[
                pip_install_requirements(),
                "pytest",
            ],
        )


class EvaluateGitTagPepe440Conformity(Job):
    def __init__(
        self,
        job_name: str = "tag-pep440-conformity",
        job_stage: str = "test",
        image: Optional[Union[Image, str]] = None,
    ) -> None:
        """
        Checks if the current pipelines `$CI_COMMIT_TAG` validates to a valid Python package version according to
        https://www.python.org/dev/peps/pep-0440

        This job already contains a rule to only run when a `$CI_COMMIT_TAG` is present (`rules.only_tags()`).
        """
        super().__init__(
            name=job_name,
            stage=job_stage,
            script="python3 -m gcip.tools.evaluate_git_tag_pep440_conformity",
        )
        self.append_rules(rules.on_tags())
        if image:
            self.set_image(image)
        else:
            self.set_image(PredefinedImages.GCIP)
