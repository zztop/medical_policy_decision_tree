from urllib import request
import io
import pymupdf4llm as pym
from urllib import parse
import re
from typing import Optional


class MedicalPolicyExtractor:

    def _download_medical_policy(self, url: str) -> Optional[str]:

        is_valid = self._validate_url(url)

        if not is_valid:
            raise Exception("Invalid url")

        try:
            with request.urlopen(url) as policy_request:
                with io.BytesIO(policy_request.read()) as data:
                    doc = pym.pymupdf.open(stream=data, filetype="pdf")
                    return pym.to_markdown(doc)
        except Exception as ex:
            raise Exception("Couldnt download file", ex)

    def _load_medical_policy(self, file_path: str) -> Optional[str]:

        try:

            with pym.pymupdf.open(file_path) as doc:
                return pym.to_markdown(doc)
        except Exception as ex:
            raise Exception("Couldnt download file", ex)

    def _validate_url(self, url: Optional[str]) -> bool:

        try:
            if url is None:
                return False
            parsed_url = parse.urlparse(url)

            return (
                parsed_url.hostname != None
                and "bluecrossma.org" in parsed_url.hostname.lower()
            )
        except:
            return False

    def _extract_medical_policy(self, policy: str) -> str:

        matched = re.search(
            "(?s)(?<=\\*\\*Policy\\*\\*)(.*?)(?=\\*\\*Prior Authorization Information\\*\\*)",
            policy,
        )
        extracted_policy_text = matched.group(1) if matched else ""

        return extracted_policy_text

    def _cleanup_medical_policy(self, policy: str) -> str:
        return policy.replace("`o`", "  -")

    def extract_medical_policy(self, file_path: str) -> str:

        is_url = file_path.upper().startswith("HTTP")

        full_policy = (
            self._download_medical_policy(file_path)
            if is_url
            else self._load_medical_policy(file_path)
        )
        policy_section = self._extract_medical_policy(full_policy or "")
        return self._cleanup_medical_policy(policy_section)


def medical_policy_extractor(url: str) -> dict[str, str]:
    """
    Extracts Medical Policy from an online medical policy document

    Args:
        url: Medical policy document url

    Returns:
        Extracted Medical Policy
    """
    return {"MEDICAL_POLICY": MedicalPolicyExtractor().extract_medical_policy(url)}
