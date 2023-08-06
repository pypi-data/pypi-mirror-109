from slai_cli import log

ERROR_MAP = {
    "existing_deployments_processing": "There are existing deployments processing, please try again in a few minutes.",  # noqa
    "no_available_model_servers": "There are currently no available model servers, please try again in a few minutes.",  # noqa
    "no_artifacts_found": "No model artifacts have been saved for this model version, please save an artifact with model_version.save() and try again.",  # noqa
}


def handle_error(*, error_msg):
    log.warn(
        f"ERROR: {ERROR_MAP.get(error_msg, f'Unknown error occured: {error_msg}')}"
    )
