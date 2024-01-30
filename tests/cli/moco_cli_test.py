import os
import subprocess

from mocogpt.cli.app import __file__ as app_file


class TestMocoGPTCli:
    def test_should_run_with_prompt(self, client):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(current_directory, "config.json")
        service_process = subprocess.Popen(
            ["python", app_file,
             "start", config_file,
             "--port", "12306"
             ])
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hi"}]
        )

        assert response.choices[0].message.content == "How can I assist you?"
        service_process.terminate()
        service_process.wait()

    def test_should_run_with_model_and_prompt(self, client):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(current_directory, "config.json")
        service_process = subprocess.Popen(
            ["python", app_file,
             "start", config_file,
             "--port", "12306"
             ])
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}]
        )

        assert response.choices[0].message.content == "How can I assist you?"
        service_process.terminate()
        service_process.wait()

    def test_should_run_with_temp_and_prompt(self, client):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(current_directory, "config.json")
        service_process = subprocess.Popen(
            ["python", app_file,
             "start", config_file,
             "--port", "12306"
             ])
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
            temperature=1.0
        )

        assert response.choices[0].message.content == "How can I assist you?"
        service_process.terminate()
        service_process.wait()
