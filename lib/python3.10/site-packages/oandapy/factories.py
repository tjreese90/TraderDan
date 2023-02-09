from simple_model.builder import model_builder


class ResponseFactory:
    """"
    Return a OANDA Response object
    """
    def __init__(self, response, endpoint=''):
        self.endpoint = endpoint
        self.response_name = self._get_response_name(endpoint)
        self.raw = response

    def __repr__(self):
        return '<{} object>'.format(self.response_name)

    def _get_response_name(self, endpoint):
        words = endpoint.split('?')[0].split('/')
        response_name = words[:1]

        if 'stream' in endpoint:
            response_name.extend(words[-2:])
        else:
            last = words[-1:]
            if '-' in last[0]:
                last = [words[-2]]

            if last != response_name:
                response_name.extend(last)
        return ''.join(word.capitalize() for word in response_name)

    def as_dict(self):
        return self.raw.json()

    def as_obj(self):
        result = self.as_dict()
        return model_builder(result)
