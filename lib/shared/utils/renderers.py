'''
This module contains the custom renderer for formating in specific way the out going request.
'''
from collections import OrderedDict
from typing import Mapping

from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .decorators import exception_handle


class MetaResponseRenderer(JSONRenderer):
    """
    Renderer class for MetaResult format.
    """

    media_type = "application/json"

    _message_key = "message"
    _success_key = "success"

    @property
    def _default_message(self):
        map_ = {
            201: "Created Successfully!",
            200: "Successfull!",
            204: "Deleted Successfully!",
            400: "Invalid request!",
            401:'Sorry, you are not authorzied for this action!'
        }
        return map_.get(self.status_code, "")

    def _add_status_message(self, resp: dict):

        if "meta" in resp:
            meta = resp.get("meta")
            if isinstance(meta, (dict, OrderedDict, Mapping)):
                if self._message_key not in meta:
                    meta[self._message_key] = self._default_message
                    meta[self._success_key] = 200 <= self.status_code <= 300

    def _parse_query_params(self, query_params: dict) -> dict:
        ret = dict()
        for k, v in query_params.items():
            if isinstance(v, (list,)):
                if len(v) == 1:
                    v = v[0]
            ret[k] = v

        return ret

    def _add_request_param(self, meta: dict, renderer_context: dict):
        if request := renderer_context.get("request"):
            meta["request"] = self._parse_query_params(
                getattr(request, "query_params", {})
            )
            if kwargs := renderer_context.get("kwargs", {}):

                if meta_ := kwargs.get("meta"):
                    meta.update(meta_)
                    kwargs.pop("meta")

                meta["request"].update(kwargs)

    def _not_legacy_format(self, data):
        return "success" not in data

    def _not_meta_format(self, data):
        return "meta" not in data

    def _attach_pagination(self, meta: dict, data: dict):
        count = data.get("count")
        next = data.get("next")
        prev = data.get("previous")

        if any([count is not None, next is not None, prev is not None]):
            meta.update(
                dict(
                    pagination=dict(
                        count=count,
                        next=next,
                        prev=prev,
                    ),
                )
            )
        return meta

    def _format_error_case(self, data):
        print("INFO: Error Case")
        resp = dict()

        meta = dict(success=False)
        if isinstance(data, (dict, OrderedDict)):
            meta["error"] = data
        else:
            meta["message"] = data
        resp["meta"] = meta
        resp["results"] = []
        return resp

    def _format_dict_case(self, data: dict):
        resp = dict()
        meta = dict(success=True)
        resp["meta"] = meta
        resp["results"] = []

        preds = [
            self._not_meta_format(data),
        ]
        if all(preds):
            if not self._not_legacy_format(data):
                data = data.get("data", data)

            if "results" not in data:  # {'id':...}
                resp["results"] = data

            else:  # {results:{'id':...},...}
                resp["results"] = data["results"]
                self._attach_pagination(meta, data)

        else:
            resp = data

        return resp

    def _format_str_case(self, data):
        resp = dict()
        meta = dict(success=True)
        resp["meta"] = meta
        meta["message"] = data
        resp["results"] = []
        return resp

    def _format_list_case(self, data):
        resp = dict()
        resp["meta"] = dict(success=True)
        resp["results"] = data
        return resp

    @exception_handle(verbose=True)
    def _to_meta_format(self, data):

        if isinstance(data, (dict, OrderedDict, str, list)):
            if 200 <= self.status_code <= 300:
                if isinstance(data, (dict, OrderedDict)):
                    data = self._format_dict_case(data)
                elif isinstance(data, list):
                    data = self._format_list_case(data)
                else:  # "Failed"
                    data = self._format_str_case(data)

            elif self.status_code >= 400:
                data = self._format_error_case(data)
        return data

    def render(self, data, media_type=None, renderer_context=None, *args, **kwargs):

        if renderer_context is not None:
            self.status_code = renderer_context["response"].status_code

        if formatted_data := self._to_meta_format(data):
            data = formatted_data

        if data is None:
            data = dict(meta=dict(), results=[])

        if isinstance(data, (dict, OrderedDict, Mapping)):
            self._add_status_message(data)
            self._add_request_param(data.get("meta", {}), renderer_context)

        try:
            data.pop("success")
        except Exception:
            ...

        return super().render(data)
