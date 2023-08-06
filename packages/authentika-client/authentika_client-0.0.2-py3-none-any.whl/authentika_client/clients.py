
from flask import Flask, jsonify, request
from requests import get, post, put, delete
from authentika_client.requests import RequestMaker
import click
import tldextract
from functools import wraps
from authentika_client.exceptions import MalformedAuthorizationHeader, InvalidAccessToken, TokenDoesNotPresentRequiredRoles, Exception403
from authentika_client.utils import requires_header_items

class AuthentikaFlaskClient(object):

    AUTHENTIKA_USE_MUST_HAVE_KEYS = [
        'AUTHENTIKA_X_API_KEY', 
    ]

    AUTHENTIKA_SUBSCRIPTION_MUST_HAVE_KEYS = [
        'AUTHENTIKA_NAME',
        'AUTHENTIKA_OWNER_EMAIL',
        'AUTHENTIKA_DESCRIPTION',
        'AUTHENTIKA_CONFIRMATION_TOKEN_EXPIRE_DT',
        'AUTHENTIKA_AUTHENTICATION_TOKEN_EXPIRE_DT',
        'AUTHENTIKA_MAX_NUM_OF_ACTIVE_TOKENS',
        'AUTHENTIKA_USER_CONFIRMATION_URL'
    ]

    AUTHENTIKA_REFRESH_TOKEN_MUST_HAVE_KEYS = [
        'AUTHENTIKA_NAME',
        'AUTHENTIKA_OWNER_EMAIL'
    ]

    def __init__(self, app):

        assert isinstance(app, Flask), "'flask_app' must be a flask.Flask instance."
        self.app = app

        self._assert_flask_config_keys_are_there(['AUTHENTIKA_BASE_URL'])
        self.request_maker = RequestMaker(self, self.app.config['AUTHENTIKA_BASE_URL'])
        
        if not self.request_maker.check_server_is_active():
            raise Exception("Authentika server is not active. So, Authentika client can not load.")
            
        self._launch_cli_commands()


    def _assert_flask_config_keys_are_there(self, list_of_keys):

        not_defined_keys = [k for k in list_of_keys if k not in self.app.config]

        assert len(not_defined_keys) == 0, "Flask app.config must have {0} defined.".format(', '.join(not_defined_keys))

    def _try_to_solve_confirmation_message_models_from_files(self,):
        
        message_models_config_keys = [
            'AUTHENTIKA_SUBSCRIPTION_CONFIRMATION_MESSAGE_MODEL', 
            'AUTHENTIKA_ACCOUNT_CHANGES_CONFIRMATION_MESSAGE_MODEL'
            ]

        for key in message_models_config_keys:

            if not key in self.app.config:

                key_path = key + '_FILE_PATH'

                if not key_path in self.app.config:

                    self.app.config[key] = None
                
                else:

                    fp = open(self.app.config[key_path], "r")
                    msg_model_str = fp.read()
                    fp.close()

                    self.app.config[key] = msg_model_str

    def _launch_cli_commands(self):

        self._try_to_solve_confirmation_message_models_from_files()

        @self.app.cli.command('subscribe-in-authentika-server')
        def subscribe_app():
        
            self._assert_flask_config_keys_are_there(self.AUTHENTIKA_SUBSCRIPTION_MUST_HAVE_KEYS)

            print("Asking for app " + self.app.config['AUTHENTIKA_NAME']  + " subscription. Please, wait...")
            
            data = self.request_maker.subscribe_app(
                name=self.app.config['AUTHENTIKA_NAME'],
                owner_email=self.app.config['AUTHENTIKA_OWNER_EMAIL'],
                description=self.app.config['AUTHENTIKA_DESCRIPTION'],
                subscription_confirmation_message_model=self.app.config['AUTHENTIKA_SUBSCRIPTION_CONFIRMATION_MESSAGE_MODEL'],
                account_changes_confirmation_message_model=self.app.config['AUTHENTIKA_ACCOUNT_CHANGES_CONFIRMATION_MESSAGE_MODEL'],
                ctoken_exp_dt_min=self.app.config['AUTHENTIKA_CONFIRMATION_TOKEN_EXPIRE_DT'],
                atoken_exp_dt_min=self.app.config['AUTHENTIKA_AUTHENTICATION_TOKEN_EXPIRE_DT'],
                max_num_of_active_tokens=self.app.config['AUTHENTIKA_MAX_NUM_OF_ACTIVE_TOKENS'],
                user_confirmation_url=self.app.config['AUTHENTIKA_USER_CONFIRMATION_URL']
            )

            return data

        @self.app.cli.command('unsubscribe-in-authentika-server')
        def unsubscribe_app():
        
            self.load_x_api_key()

            print("Asking for app " + self.app.config['AUTHENTIKA_NAME']  + " unsubscription. Please, wait...")
            
            data = self.request_maker.unsubscribe_app()

            return data

        @self.app.cli.command('refresh-my-authentika-x-api-key')
        def refresh_app_x_api_key():
            
            self._assert_flask_config_keys_are_there(self.AUTHENTIKA_REFRESH_TOKEN_MUST_HAVE_KEYS)

            self.load_x_api_key()

            data = self.request_maker.refresh_x_api_key(
                name=self.app.config['AUTHENTIKA_NAME'],
                owner_email=self.app.config['AUTHENTIKA_OWNER_EMAIL']
            )

            return data


    def launch_me(self):

        self.update_app()

        my_data = self.get_my_data()

        self._assert_flask_config_keys_are_there(self.AUTHENTIKA_USE_MUST_HAVE_KEYS)

        user_confirmation_url_parsed = tldextract.extract(my_data['data']['attributes']['user_confirmation_url'])

        user_confirmation_sub_path ='/'+'/'.join(my_data['data']['attributes']['user_confirmation_url'].split(user_confirmation_url_parsed.domain)[-1].split('/')[1:]) + "<string:confirmation_token>"

        self.app.add_url_rule(user_confirmation_sub_path, view_func=self._confirm_operation_by_token)


    def load_x_api_key(self,):

        self._assert_flask_config_keys_are_there(self.AUTHENTIKA_USE_MUST_HAVE_KEYS)
        self.x_api_key = self.app.config['AUTHENTIKA_X_API_KEY']

    def update_app(self,):
        
        self._assert_flask_config_keys_are_there(self.AUTHENTIKA_SUBSCRIPTION_MUST_HAVE_KEYS)

        self.load_x_api_key()

        print("Asking for app " + self.app.config['AUTHENTIKA_NAME']  + " features updating. Please, wait...")
        
        data = self.request_maker.update_app_features(
            name=self.app.config['AUTHENTIKA_NAME'],
            description=self.app.config['AUTHENTIKA_DESCRIPTION'],
            subscription_confirmation_message_model=self.app.config['AUTHENTIKA_SUBSCRIPTION_CONFIRMATION_MESSAGE_MODEL'],
            account_changes_confirmation_message_model=self.app.config['AUTHENTIKA_ACCOUNT_CHANGES_CONFIRMATION_MESSAGE_MODEL'],
            ctoken_exp_dt_min=self.app.config['AUTHENTIKA_CONFIRMATION_TOKEN_EXPIRE_DT'],
            atoken_exp_dt_min=self.app.config['AUTHENTIKA_AUTHENTICATION_TOKEN_EXPIRE_DT'],
            max_num_of_active_tokens=self.app.config['AUTHENTIKA_MAX_NUM_OF_ACTIVE_TOKENS'],
            user_confirmation_url=self.app.config['AUTHENTIKA_USER_CONFIRMATION_URL']
        )

        return True

    def get_my_data(self,):
        self.load_x_api_key()
        data = self.request_maker.get_app()
        return data

    def subscribe_user_by_email(self, email, password, presentation_name=None):

        data = self.request_maker.subscribe_user_by_email(
            email=email,
            password=password,
            presentation_name=presentation_name
        )

        return data

    def _confirm_operation_by_token(self, confirmation_token):
        
        data, status_code = self.request_maker.confirm_operation_by_token(confirmation_token)

        return jsonify(data), status_code

    def get_user_by_email(self, email):

        data = self.request_maker.get_user_by_email(email)
        return data

    def delete_user_by_email(self, email):

        data = self.request_maker.delete_user_by_email(email)
        return data

    def emit_user_token_with_roles_by_email(self, email, password, roles=None):
        
        payload = {'roles': roles}
        data = self.request_maker.emit_user_token_by_email(email, password, payload)
        return data
        
    def invalidate_user_token(self, token):
        data = self.request_maker.invalidate_user_token(token)
        return data

    def open_user_token(self, token):
        data = self.request_maker.open_user_token(token)
        return data

    def refresh_user_token(self, token):
        data = self.request_maker.refresh_user_token(token)
        return data

    def invalidate_all_tokens_for_this_user(self, email):
        data = self.request_maker.invalidate_all_tokens_for_this_user(email)
        return data
    
    def invalidate_all_tokens_for_this_app(self):
        data = self.request_maker.invalidate_all_tokens_for_this_app()
        return data

    def update_user_data_by_email(self, current_email, current_password, new_email=None, new_password=None):

        data = self.request_maker.update_user_data_by_email(current_email, current_password, new_email, new_password)
        return data

    def lock_user_by_email_to_create_tokens(self, email):

        data = self.request_maker.lock_user_by_email_to_create_tokens(email)
        return data

    def unlock_user_by_email_to_create_tokens(self, email):

        data = self.request_maker.unlock_user_by_email_to_create_tokens(email)
        return data

    def check_user_roles(self, required_roles=None, **kwargs):  
        def wrapper(fn):
            @wraps(fn)
            @requires_header_items(['Authorization'])
            def decorated_fun(*args, **kwargs):
                auth_header = kwargs['Authorization']
                try:
                    auth_token = auth_header.split("Bearer")[1].strip()

                    data = self.open_user_token(auth_token)

                    if required_roles:
                        for role in required_roles:
                            if not role in data['data']['attributes']['payload']['roles']:
                                raise TokenDoesNotPresentRequiredRoles("Access token doesn't present some required roles.")
                    
                    kwargs['user_data'] = data['data']
                    kwargs['user_valid_access_token'] = auth_token
                    return fn(*args, **kwargs)

                except Exception403:
                    raise InvalidAccessToken("Invalid user's access token.")

                except IndexError:
                    raise MalformedAuthorizationHeader('Authorization header is malformed. It must be something like "Bearer <ACCESS-TOKEN>".')
                    
            return decorated_fun
        return wrapper

    def my_login_route(self, user_roles_definition_function=None):
        def wrapper(fn):
            @wraps(fn)
            def decorated_fun(*args, **kwargs):

                email = request.authorization['username']
                password = request.authorization['password']
                kwargs['valid_token_data'] = self.emit_user_token_with_roles_by_email(
                    email,
                    password,
                    user_roles_definition_function(email) if user_roles_definition_function else None)
                return fn(*args, **kwargs)

            return decorated_fun
        return wrapper
                

    def my_logout_route(self, *args, **kwargs):
        
        def wrapper(fn):
            @wraps(fn)
            @self.check_user_roles()
            def decorated_fun(*args, **kwargs): 
                
                user_valid_access_token = kwargs['user_valid_access_token']
                self.invalidate_user_token(user_valid_access_token)
                return fn(*args, **kwargs)
        
            return decorated_fun
        return wrapper
                
    


    

    