import pytest
from openai import BadRequestError, OpenAI

from mocogpt import any_of, gpt_server, none_of


class TestChatCompletions:
    def test_should_reply_content_for_specified_prompt(self, client: OpenAI):
        server = gpt_server(12306)
        server.chat.completions.request(prompt="Hi").response(content="How can I assist you?")

        with server:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "Hi"}]
            )

            assert response.choices[0].message.content == "How can I assist you?"

    def test_should_reply_content_for_specified_prompt_in_stream(self, client: OpenAI):
        server = gpt_server(12306)
        server.chat.completions.request(prompt="Hi").response(content="How can I assist you?")

        with server:
            stream = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "Hi"}],
                stream=True
            )

            result = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    result = result + chunk.choices[0].delta.content

            assert result == "How can I assist you?"

    def test_should_not_reply_anything(self, client: OpenAI):
        server = gpt_server(12306)

        with server:
            with pytest.raises(BadRequestError):
                client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": "Hi"}]
                )

    def test_should_reply_content_for_specified_prompt_and_model(self, client: OpenAI):
        server = gpt_server(12306)
        server.chat.completions.request(prompt="Hi", model="gpt-4").response(content="How can I assist you?")

        with server:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "Hi"}]
            )

            assert response.choices[0].message.content == "How can I assist you?"

    def test_should_reply_content_for_specified_prompt_or_model(self, client: OpenAI):
        server = gpt_server(12306)
        server.chat.completions.request(
            prompt="Hello", model="gpt-4"
        ).or_request(
            prompt="Hi", model="gpt-3.5-turbo-1106"
        ).response(content="How can I assist you?")

        with server:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=[{"role": "user", "content": "Hi"}]
            )

            assert response.choices[0].message.content == "How can I assist you?"

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "Hello"}]
            )

            assert response.choices[0].message.content == "How can I assist you?"

    def test_should_reply_content_for_specified_temperature(self, client: OpenAI):
        server = gpt_server(12306)
        server.chat.completions.request(temperature=1.0).response(content="How can I assist you?")

        with server:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=[{"role": "user", "content": "Hi"}],
                temperature=1.0
            )

            assert response.choices[0].message.content == "How can I assist you?"

    def test_should_reply_content_for_specified_api_key(self, client: OpenAI):
        server = gpt_server(12306)
        server.chat.completions.request(api_key="sk-123456789", prompt="Hi").response(content="Hi")
        server.chat.completions.request(api_key="sk-987654321", prompt="Hi").response(content="Hello")

        with server:
            client = OpenAI(base_url="http://localhost:12306/v1", api_key="sk-123456789")
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "Hi"}]
            )

            assert response.choices[0].message.content == "Hi"

            client = OpenAI(base_url="http://localhost:12306/v1", api_key="sk-987654321")
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "Hi"}]
            )

            assert response.choices[0].message.content == "Hello"

    def test_should_reply_content_for_specified_any_prompt(self, client: OpenAI):
        server = gpt_server(12306)
        server.chat.completions.request(prompt=any_of("Hi", "Hello")).response(content="How can I assist you?")

        with server:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "Hi"}]
            )

            assert response.choices[0].message.content == "How can I assist you?"

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "Hello"}]
            )

            assert response.choices[0].message.content == "How can I assist you?"

    def test_should_reply_content_for_non_prompt(self, client: OpenAI):
        server = gpt_server(12306)
        server.chat.completions.request(prompt=none_of("Hi", "Hello")).response(content="How can I assist you?")

        with server:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "Nice to meet you"}]
            )

            assert response.choices[0].message.content == "How can I assist you?"

            with pytest.raises(BadRequestError):
                client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": "Hi"}]
                )

    def test_should_raise_exception_for_unknown_config(self):
        server = gpt_server(12306)
        with pytest.raises(TypeError):
            server.chat.completions.request(unknown="Hi").response(content="How can I assist you?")

        with pytest.raises(TypeError):
            server.chat.completions.request(prompt="Hi").response(unknown="Hi")
