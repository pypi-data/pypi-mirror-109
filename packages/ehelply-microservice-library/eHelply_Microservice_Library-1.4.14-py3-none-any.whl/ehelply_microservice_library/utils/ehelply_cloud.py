import asyncio
import traceback

from typing import Union, Optional

import sentry_sdk

from pydantic import BaseModel

from fastapi import HTTPException

from ehelply_bootstrapper.utils.state import State

from ehelply_python_sdk.services.access.auth_rules import AuthRule, AuthException
from ehelply_python_sdk.services.access.sdk import AuthModel, is_response_error

from ehelply_microservice_library.integrations.monitor import Monitor
from ehelply_microservice_library.integrations.m2m import M2M


class CloudParticipant(BaseModel):
    active_participant: str
    project_uuid: str
    is_privileged: bool = False
    entity_identifier: Optional[str] = None


async def ehelply_cloud_access(
        auth: AuthModel,
        node: str,
        service_target: str,
        monitor: Monitor,
        ignore_project_enabled=False,
        ignore_spend_limits=False,
        exception_if_unauthorized=True,
        exception_if_spend_maxed=True,
        exception_if_project_not_enabled=True,
        i_am_monitor=False,
) -> Union[bool, CloudParticipant]:
    """

    Args:
        auth:
        node:
        service_target:
        monitor: Send in the monitor integration and project max spend will be checked automatically
        exception_if_unauthorized:
        exception_if_spend_maxed:

    Returns:

    """

    with sentry_sdk.start_span(op="cp_authorization", description="CloudParticipant Authorization") as span:

        # If key is a known M2M key to this service, we can just return right out of this
        m2m_integration: M2M = State.integrations.get("m2m")
        if m2m_integration.speedy_m2m_auth(access_token=auth.access_token, secret_token=auth.secret_token):
            return CloudParticipant(
                is_privileged=True,
                active_participant=auth.active_participant_uuid,
                project_uuid=auth.project_uuid,
                entity_identifier=auth.entity_identifier
            )

        # API Requests
        admin_auth = asyncio.create_task(AuthRule(
            auth,
            exception_if_unauthorized=False
        ).participant_has_node_on_target(
            node=node,
            target_identifier=service_target,
            partition="ehelply-resources"
        ).verify())

        cloud_auth = asyncio.create_task(AuthRule(
            auth,
            exception_if_unauthorized=False
        ).participant_has_node_on_target(
            node=node,
            target_identifier=auth.project_uuid,
            partition="ehelply-cloud"
        ).customentity_has_node_on_target(
            node=node,
            target_identifier=service_target,
            partition="ehelply-cloud",
            entity_identifier=auth.project_uuid
        ).verify())

        if not i_am_monitor:
            project = asyncio.create_task(
                monitor.get_project(project_uuid=auth.project_uuid)
            )

        try:
            if not i_am_monitor:
                api_results = await asyncio.gather(admin_auth, cloud_auth, project)
            else:
                api_results = await asyncio.gather(admin_auth, cloud_auth)
        except Exception as e:
            traceback.print_exc()
            State.logger.warning(message="cloud_participant async gather failed. In the past this was due to ehelply-access not responding correctly, but this could occur for other unknown reasons as well.")
            raise HTTPException(
                status_code=500,
                detail="Big sad, something has gone terribly wrong - Denied by eHelply."
            )

        admin_auth = api_results[0]
        cloud_auth = api_results[1]

        if not i_am_monitor:
            project = api_results[2]

        # Admin or M2M access
        try:
            # await AuthRule(
            #     auth,
            #     exception_if_unauthorized=True
            # ).participant_has_node_on_target(
            #     node=node,
            #     target_identifier=service_target,
            #     partition="ehelply-resources"
            # ).verify()
            if not admin_auth:
                raise AuthException()

            return CloudParticipant(
                is_privileged=True,
                active_participant=auth.active_participant_uuid,
                project_uuid=auth.project_uuid,
                entity_identifier=auth.entity_identifier
            )
        except (AuthException, HTTPException):
            pass
        except Exception as e:
            traceback.print_exc()
            State.logger.warning(message="cloud_participant admin/m2m access checks caused an unexpected error.")
            raise HTTPException(
                status_code=500,
                detail="Ruh Roh, something has gone terribly wrong - Denied by eHelply."
            )

        spend_maxed: bool = False
        project_not_enabled: bool = False

        # Regular eHelply Cloud access
        try:
            # await AuthRule(
            #     auth,
            #     exception_if_unauthorized=True
            # ).participant_has_node_on_target(
            #     node=node,
            #     target_identifier=auth.project_uuid,
            #     partition="ehelply-cloud"
            # ).customentity_has_node_on_target(
            #     node=node,
            #     target_identifier=service_target,
            #     partition="ehelply-cloud",
            #     entity_identifier=auth.project_uuid
            # ).verify()
            if not cloud_auth:
                raise AuthException()

            if not i_am_monitor:
                # project = await monitor.get_project(project_uuid=auth.project_uuid)
                if not project or is_response_error(project):
                    raise AuthException()

                if not ignore_project_enabled and project.status != "enabled":
                    project_not_enabled = True
                    raise AuthException("Project is not enabled")

                if not ignore_spend_limits and project.is_spend_maxed:
                    spend_maxed = True
                    raise AuthException("Spend is maxed")

            return CloudParticipant(
                is_privileged=False,
                active_participant=auth.active_participant_uuid,
                project_uuid=auth.project_uuid,
                entity_identifier=auth.entity_identifier
            )
        except (AuthException, HTTPException):
            pass
        except Exception as e:
            traceback.print_exc()
            State.logger.warning(message="cloud_participant regular ehelply cloud access checks caused an unexpected error.")
            raise HTTPException(
                status_code=500,
                detail="Ruh Roh, something has gone terribly wrong - Denied by eHelply."
            )

        if spend_maxed and exception_if_spend_maxed:
            raise HTTPException(
                status_code=400,
                detail="Project spend is maxed - Denied by eHelply. Increase max spend to complete this request."
            )
        elif spend_maxed:
            return False

        if project_not_enabled and exception_if_project_not_enabled:
            raise HTTPException(
                status_code=400,
                detail="Project is not enabled - Denied by eHelply. The project may be awaiting approval or disabled."
            )
        elif project_not_enabled:
            return False

        if exception_if_unauthorized:
            raise HTTPException(status_code=403, detail="Unauthorized - Denied by eHelply")
        else:
            return False

        #
        # return AuthRule(
        #     auth,
        #     AuthRule(auth).participant_has_node_on_target(
        #         node=node,
        #         target_identifier=service_target,
        #         partition="ehelply-resources"
        #     ),
        #     AuthRule(auth).participant_has_node_on_target(
        #         node=node,
        #         target_identifier=auth.project_uuid,
        #         partition="ehelply-cloud"
        #     ).customentity_has_node_on_target(
        #         node=node,
        #         target_identifier=service_target,
        #         partition="ehelply-cloud",
        #         entity_identifier=auth.project_uuid
        #     ),
        #     exception_if_unauthorized=exception_if_unauthorized
        # ).verify()
