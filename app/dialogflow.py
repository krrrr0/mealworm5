from app.log import Logger

import dialogflow_v2 as dialogflow

from google.oauth2 import service_account


credentials = service_account.Credentials.from_service_account_file('mealworm5-630b8064ec70.json')
session_client = dialogflow.SessionsClient(credentials=credentials)
entity_client = dialogflow.SessionEntityTypesClient(credentials=credentials)


class DialogFlowController:
    def __init__(self, g_config):
        self.project_id = g_config['DIALOGFLOW']['PROJECT_ID']
        return

    def get_results(self, query, user_id, session):
        session = session_client.session_path(self.project_id, user_id + session)
        text_input = dialogflow.types.TextInput(text=query, language_code='ko_KR')
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

        Logger.log('[DF > get_intent] Dialogflow API 처리 완료!', 'NOTICE', '요청 query: %s' % query)

        entities = {}
        for e in response.query_result.parameters.fields:
            entities[e] = response.query_result.parameters.fields.get(e).string_value

        return {
            'intent': response.query_result.intent.display_name,
            'confidence': response.query_result.intent_detection_confidence,
            'entities': entities
        }
