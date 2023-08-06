from requests import get, post, put, delete
from authentika_client.exceptions import Exception422, Exception405, Exception404, Exception403, Exception401


def solve_response(response,):

    def _map_exception_message(e, status_code, data):

        exception_str = "status: " + str(response.status_code) + "\nNot mapped exception!!"
        if data:
            exception_str = "status: " + str(response.status_code) + "\n" + '\n'.join([err['detail'] for err in data['data']['attributes']['errors']])
        
        raise e(exception_str)

    try:
        data = response.json()
    except Exception:
        data = None
    finally:
        if response.status_code in [200, 201, 203]:
            return data
        elif response.status_code == 422:
            _map_exception_message(Exception422, 422, data)
        elif response.status_code == 405:
            _map_exception_message(Exception405, 405, data)
        elif response.status_code == 404:
            _map_exception_message(Exception404, 404, data)
        elif response.status_code == 403:
            _map_exception_message(Exception403, 404, data)
        elif response.status_code == 401:
            _map_exception_message(Exception401, 401, data)
        else:
            _map_exception_message(Exception, 500, data)

class RequestMaker(object):

    def __init__(self, authentika_client_app, base_url):

        self._base_url = base_url
        self._authentika_client_app = authentika_client_app
    
    def check_server_is_active(self,):

        r = get(
            self._base_url + "/hello"
        )

        if r.status_code == 200:
            return True
        else:
            return False

    def subscribe_app(self, name, owner_email, description, ctoken_exp_dt_min,
     atoken_exp_dt_min, max_num_of_active_tokens, user_confirmation_url,
      subscription_confirmation_message_model=None, account_changes_confirmation_message_model=None):

        attributes = {
            'name': name,
            'owner_email': owner_email,
            'description': description,
            'subscription_confirmation_message_model': subscription_confirmation_message_model,
            'account_changes_confirmation_message_model': account_changes_confirmation_message_model,
            'ctoken_exp_dt_min': ctoken_exp_dt_min,
            'atoken_exp_dt_min': atoken_exp_dt_min,
            'max_num_of_active_tokens': max_num_of_active_tokens,
            'user_confirmation_url': user_confirmation_url
        }

        r = post(
            self._base_url + "/apps/subscription",
            json={
                'data': {
                    'type': "app-subscription",
                    'attributes': attributes
                }           
            }
        )

        return solve_response(r)

    def refresh_x_api_key(self, name, owner_email):

        attributes = {
            'name': name,
            'owner_email': owner_email
        }

        r = put(
            self._base_url + "/apps/refresh-credentials",
            json={
                'data': {
                    'type': "app-credentials-refresh",
                    'attributes': attributes
                }
               
            },
        )

        return solve_response(r)

    def update_app_features(self, name, description, ctoken_exp_dt_min, atoken_exp_dt_min,
     max_num_of_active_tokens, user_confirmation_url, 
     subscription_confirmation_message_model=None, account_changes_confirmation_message_model=None):
        
        headers = {"X-Api-Key": self._authentika_client_app.x_api_key}

        attributes = {
            'name': name,
            'description': description,
            'subscription_confirmation_message_model': subscription_confirmation_message_model,
            'account_changes_confirmation_message_model': account_changes_confirmation_message_model,
            'ctoken_exp_dt_min': ctoken_exp_dt_min,
            'atoken_exp_dt_min': atoken_exp_dt_min,
            'max_num_of_active_tokens': max_num_of_active_tokens,
            'user_confirmation_url': user_confirmation_url
        }

        r = put(
            self._base_url + "/apps",
            json={
                'data': {
                    'type': "app-updating",
                    'attributes': attributes
                }
            },
            headers=headers
        )

        return solve_response(r)

    def unsubscribe_app(self,):
        headers = {"X-Api-Key": self._authentika_client_app.x_api_key}

        r = delete(
            self._base_url + "/apps/unsubscription",
            headers=headers
        )

        return solve_response(r)


    def get_app(self,):

        headers = {"X-Api-Key": self._authentika_client_app.x_api_key}

        r = get(self._base_url + "/apps", headers=headers)

        return solve_response(r)
        

    def subscribe_user_by_email(self, email, password, presentation_name=None):
        
        headers = {"X-Api-Key": self._authentika_client_app.x_api_key}

        attributes = {
            'email': email,
            'password': password,
            'presentation_name': presentation_name
        }

        r = post(
            self._base_url + "/app-users/subscription-by-email",
            json={
                'data': {
                    'type': "app-user-subscription-by-email",
                    'attributes': attributes
                }
            }, 
            headers=headers
        )

        return solve_response(r)

    def confirm_operation_by_token(self, confirmation_token):
        
        headers = {"X-Api-Key": self._authentika_client_app.x_api_key}

        r = get(
            self._base_url + '/app-users/subscription-by-email/' + confirmation_token,
            headers=headers
        )

        return solve_response(r), r.status_code
    
    def get_user_by_email(self, email):

        headers = {"X-Api-Key": self._authentika_client_app.x_api_key}

        r = get(
            self._base_url + '/app-users/management-by-email/' + str(email),
            headers=headers
        )

        return solve_response(r)

    def delete_user_by_email(self, email):

        headers = {"X-Api-Key": self._authentika_client_app.x_api_key}

        r = delete(
            self._base_url + '/app-users/management-by-email/' + str(email),
            headers=headers
        )

        return solve_response(r)

    def emit_user_token_by_email(self, email, password, payload=None):

        headers = {"X-Api-Key": self._authentika_client_app.x_api_key}

        attributes = {
            'email': email,
            'password': password,
            'payload': payload
        }

        r = post(
            self._base_url + '/app-users/create-a-token',
            json={
                'data': {
                    'type': "app-user-token-creation-by-email",
                    'attributes': attributes
                }
            }, 
            headers=headers
        )

        return solve_response(r)

    def invalidate_user_token(self, token):

        headers = {"X-Api-Key": self._authentika_client_app.x_api_key}
        
        r = delete(
            self._base_url + '/app-user-token/' + str(token),
            headers=headers
        )

        return solve_response(r)

    def refresh_user_token(self, token):

        headers = {"X-Api-Key": self._authentika_client_app.x_api_key}
        
        r = put(
            self._base_url + '/app-user-token/' + str(token),
            headers=headers
        )

        return solve_response(r)


    def open_user_token(self, token):

        headers = {"X-Api-Key": self._authentika_client_app.x_api_key}
        
        r = get(
            self._base_url + '/app-user-token/' + str(token),
            headers=headers
        )

        return solve_response(r)

    def invalidate_all_tokens_for_this_user(self, email):

        headers = {"X-Api-Key": self._authentika_client_app.x_api_key}

        r = delete(
            self._base_url + "/app-users/" + str(email) + "/active-tokens",
            headers=headers
        )

        return solve_response(r)
    
    def invalidate_all_tokens_for_this_app(self):

        headers = {"X-Api-Key": self._authentika_client_app.x_api_key}

        r = delete(
            self._base_url + "/apps/active-tokens",
            headers=headers
        )
        
        return solve_response(r)

    def lock_user_by_email_to_create_tokens(self, email):
        
        headers = {"X-Api-Key": self._authentika_client_app.x_api_key}

        r = put(
            self._base_url + "/app-users/" + str(email) + "/lock",
            headers=headers
        )

        return solve_response(r)

    def unlock_user_by_email_to_create_tokens(self, email):
        
        headers = {"X-Api-Key": self._authentika_client_app.x_api_key}

        r = delete(
            self._base_url + "/app-users/" + str(email) + "/lock",
            headers=headers
        )

        return solve_response(r)

    def update_user_data_by_email(self, current_email, current_password, new_email=None, new_password=None):

        headers = {"X-Api-Key": self._authentika_client_app.x_api_key}

        attributes ={
            'current_email': current_email,
            'current_password': current_password,
            'new_email': new_email,
            'new_password': new_password
        }

        r = put(
            self._base_url + '/app-users/management-by-email',
            json={
                'data': {
                    'type': "app-user-account-management-by-email",
                    'attributes': attributes
                }
            }, 
            headers=headers
        )

        return solve_response(r)

        



