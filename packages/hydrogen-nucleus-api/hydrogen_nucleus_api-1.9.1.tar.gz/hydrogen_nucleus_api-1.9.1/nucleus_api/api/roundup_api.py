# coding: utf-8

"""
    Hydrogen Nucleus API

    The Hydrogen Nucleus API  # noqa: E501

    OpenAPI spec version: 1.9.0
    Contact: info@hydrogenplatform.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from nucleus_api.api_client import ApiClient


class RoundupApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_roundup_settings_using_post(self, roundup_settings, **kwargs):  # noqa: E501
        """Create a Roundup Settings  # noqa: E501

        Create a Roundup Settings for Roundup amount with your firm.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_roundup_settings_using_post(roundup_settings, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param RoundupSettings roundup_settings: roundupSettings (required)
        :return: RoundupSettings
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_roundup_settings_using_post_with_http_info(roundup_settings, **kwargs)  # noqa: E501
        else:
            (data) = self.create_roundup_settings_using_post_with_http_info(roundup_settings, **kwargs)  # noqa: E501
            return data

    def create_roundup_settings_using_post_with_http_info(self, roundup_settings, **kwargs):  # noqa: E501
        """Create a Roundup Settings  # noqa: E501

        Create a Roundup Settings for Roundup amount with your firm.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_roundup_settings_using_post_with_http_info(roundup_settings, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param RoundupSettings roundup_settings: roundupSettings (required)
        :return: RoundupSettings
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['roundup_settings']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_roundup_settings_using_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'roundup_settings' is set
        if self.api_client.client_side_validation and ('roundup_settings' not in params or
                                                       params['roundup_settings'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `roundup_settings` when calling `create_roundup_settings_using_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'roundup_settings' in params:
            body_params = params['roundup_settings']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth2']  # noqa: E501

        return self.api_client.call_api(
            '/nucleus/v1/roundup_setting', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RoundupSettings',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_roundup_using_post(self, roundup_co, **kwargs):  # noqa: E501
        """Create a roundup  # noqa: E501

        Create a new roundup with your firm.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_roundup_using_post(roundup_co, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param RoundupCO roundup_co: roundupCO (required)
        :return: Roundup
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_roundup_using_post_with_http_info(roundup_co, **kwargs)  # noqa: E501
        else:
            (data) = self.create_roundup_using_post_with_http_info(roundup_co, **kwargs)  # noqa: E501
            return data

    def create_roundup_using_post_with_http_info(self, roundup_co, **kwargs):  # noqa: E501
        """Create a roundup  # noqa: E501

        Create a new roundup with your firm.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_roundup_using_post_with_http_info(roundup_co, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param RoundupCO roundup_co: roundupCO (required)
        :return: Roundup
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['roundup_co']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_roundup_using_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'roundup_co' is set
        if self.api_client.client_side_validation and ('roundup_co' not in params or
                                                       params['roundup_co'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `roundup_co` when calling `create_roundup_using_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'roundup_co' in params:
            body_params = params['roundup_co']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth2']  # noqa: E501

        return self.api_client.call_api(
            '/nucleus/v1/roundup', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Roundup',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_roundup_settings_using_delete(self, roundup_setting_id, **kwargs):  # noqa: E501
        """Delete a roundup settings  # noqa: E501

        Permanently delete a  roundup settings registered with your firm.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_roundup_settings_using_delete(roundup_setting_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str roundup_setting_id: UUID roundup_setting_id (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_roundup_settings_using_delete_with_http_info(roundup_setting_id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_roundup_settings_using_delete_with_http_info(roundup_setting_id, **kwargs)  # noqa: E501
            return data

    def delete_roundup_settings_using_delete_with_http_info(self, roundup_setting_id, **kwargs):  # noqa: E501
        """Delete a roundup settings  # noqa: E501

        Permanently delete a  roundup settings registered with your firm.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_roundup_settings_using_delete_with_http_info(roundup_setting_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str roundup_setting_id: UUID roundup_setting_id (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['roundup_setting_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_roundup_settings_using_delete" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'roundup_setting_id' is set
        if self.api_client.client_side_validation and ('roundup_setting_id' not in params or
                                                       params['roundup_setting_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `roundup_setting_id` when calling `delete_roundup_settings_using_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'roundup_setting_id' in params:
            path_params['roundup_setting_id'] = params['roundup_setting_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth2']  # noqa: E501

        return self.api_client.call_api(
            '/nucleus/v1/roundup_setting/{roundup_setting_id}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_roundup_all_using_get(self, **kwargs):  # noqa: E501
        """List all roundups  # noqa: E501

        Get details for all roundups.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_roundup_all_using_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool ascending: ascending
        :param str filter: filter
        :param str order_by: order_by
        :param int page: page
        :param int size: size
        :return: PageRoundup
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_roundup_all_using_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_roundup_all_using_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_roundup_all_using_get_with_http_info(self, **kwargs):  # noqa: E501
        """List all roundups  # noqa: E501

        Get details for all roundups.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_roundup_all_using_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool ascending: ascending
        :param str filter: filter
        :param str order_by: order_by
        :param int page: page
        :param int size: size
        :return: PageRoundup
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['ascending', 'filter', 'order_by', 'page', 'size']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_roundup_all_using_get" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'ascending' in params:
            query_params.append(('ascending', params['ascending']))  # noqa: E501
        if 'filter' in params:
            query_params.append(('filter', params['filter']))  # noqa: E501
        if 'order_by' in params:
            query_params.append(('order_by', params['order_by']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'size' in params:
            query_params.append(('size', params['size']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth2']  # noqa: E501

        return self.api_client.call_api(
            '/nucleus/v1/roundup', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PageRoundup',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_roundup_settings_all_using_get(self, **kwargs):  # noqa: E501
        """List all roundup settings  # noqa: E501

        Get details for all roundup setting with your firm.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_roundup_settings_all_using_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool ascending: ascending
        :param str filter: filter
        :param str order_by: order_by
        :param int page: page
        :param int size: size
        :return: PageRoundupSettings
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_roundup_settings_all_using_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_roundup_settings_all_using_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_roundup_settings_all_using_get_with_http_info(self, **kwargs):  # noqa: E501
        """List all roundup settings  # noqa: E501

        Get details for all roundup setting with your firm.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_roundup_settings_all_using_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool ascending: ascending
        :param str filter: filter
        :param str order_by: order_by
        :param int page: page
        :param int size: size
        :return: PageRoundupSettings
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['ascending', 'filter', 'order_by', 'page', 'size']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_roundup_settings_all_using_get" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'ascending' in params:
            query_params.append(('ascending', params['ascending']))  # noqa: E501
        if 'filter' in params:
            query_params.append(('filter', params['filter']))  # noqa: E501
        if 'order_by' in params:
            query_params.append(('order_by', params['order_by']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'size' in params:
            query_params.append(('size', params['size']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth2']  # noqa: E501

        return self.api_client.call_api(
            '/nucleus/v1/roundup_setting', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PageRoundupSettings',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_roundup_settings_using_get(self, roundup_setting_id, **kwargs):  # noqa: E501
        """Retrieve a Roundup Setting  # noqa: E501

        Retrieve the information for a Roundup Settings with your firm.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_roundup_settings_using_get(roundup_setting_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str roundup_setting_id: UUID roundup_setting_id (required)
        :return: RoundupSettings
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_roundup_settings_using_get_with_http_info(roundup_setting_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_roundup_settings_using_get_with_http_info(roundup_setting_id, **kwargs)  # noqa: E501
            return data

    def get_roundup_settings_using_get_with_http_info(self, roundup_setting_id, **kwargs):  # noqa: E501
        """Retrieve a Roundup Setting  # noqa: E501

        Retrieve the information for a Roundup Settings with your firm.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_roundup_settings_using_get_with_http_info(roundup_setting_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str roundup_setting_id: UUID roundup_setting_id (required)
        :return: RoundupSettings
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['roundup_setting_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_roundup_settings_using_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'roundup_setting_id' is set
        if self.api_client.client_side_validation and ('roundup_setting_id' not in params or
                                                       params['roundup_setting_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `roundup_setting_id` when calling `get_roundup_settings_using_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'roundup_setting_id' in params:
            path_params['roundup_setting_id'] = params['roundup_setting_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth2']  # noqa: E501

        return self.api_client.call_api(
            '/nucleus/v1/roundup_setting/{roundup_setting_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RoundupSettings',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_roundup_using_get(self, roundup_id, **kwargs):  # noqa: E501
        """Retrieve a Roundup  # noqa: E501

        Retrieve the information for a Roundup.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_roundup_using_get(roundup_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str roundup_id: UUID roundup_id (required)
        :return: Roundup
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_roundup_using_get_with_http_info(roundup_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_roundup_using_get_with_http_info(roundup_id, **kwargs)  # noqa: E501
            return data

    def get_roundup_using_get_with_http_info(self, roundup_id, **kwargs):  # noqa: E501
        """Retrieve a Roundup  # noqa: E501

        Retrieve the information for a Roundup.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_roundup_using_get_with_http_info(roundup_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str roundup_id: UUID roundup_id (required)
        :return: Roundup
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['roundup_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_roundup_using_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'roundup_id' is set
        if self.api_client.client_side_validation and ('roundup_id' not in params or
                                                       params['roundup_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `roundup_id` when calling `get_roundup_using_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'roundup_id' in params:
            path_params['roundup_id'] = params['roundup_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth2']  # noqa: E501

        return self.api_client.call_api(
            '/nucleus/v1/roundup/{roundup_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Roundup',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_roundup_settings_using_put(self, roundup_setting, roundup_setting_id, **kwargs):  # noqa: E501
        """Update a roundup settings  # noqa: E501

        Update the information for a roundup setting registered with your firm.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_roundup_settings_using_put(roundup_setting, roundup_setting_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object roundup_setting: roundup_setting (required)
        :param str roundup_setting_id: UUID roundup_setting_id (required)
        :return: RoundupSettings
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_roundup_settings_using_put_with_http_info(roundup_setting, roundup_setting_id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_roundup_settings_using_put_with_http_info(roundup_setting, roundup_setting_id, **kwargs)  # noqa: E501
            return data

    def update_roundup_settings_using_put_with_http_info(self, roundup_setting, roundup_setting_id, **kwargs):  # noqa: E501
        """Update a roundup settings  # noqa: E501

        Update the information for a roundup setting registered with your firm.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_roundup_settings_using_put_with_http_info(roundup_setting, roundup_setting_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param object roundup_setting: roundup_setting (required)
        :param str roundup_setting_id: UUID roundup_setting_id (required)
        :return: RoundupSettings
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['roundup_setting', 'roundup_setting_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_roundup_settings_using_put" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'roundup_setting' is set
        if self.api_client.client_side_validation and ('roundup_setting' not in params or
                                                       params['roundup_setting'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `roundup_setting` when calling `update_roundup_settings_using_put`")  # noqa: E501
        # verify the required parameter 'roundup_setting_id' is set
        if self.api_client.client_side_validation and ('roundup_setting_id' not in params or
                                                       params['roundup_setting_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `roundup_setting_id` when calling `update_roundup_settings_using_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'roundup_setting_id' in params:
            path_params['roundup_setting_id'] = params['roundup_setting_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'roundup_setting' in params:
            body_params = params['roundup_setting']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth2']  # noqa: E501

        return self.api_client.call_api(
            '/nucleus/v1/roundup_setting/{roundup_setting_id}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RoundupSettings',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
