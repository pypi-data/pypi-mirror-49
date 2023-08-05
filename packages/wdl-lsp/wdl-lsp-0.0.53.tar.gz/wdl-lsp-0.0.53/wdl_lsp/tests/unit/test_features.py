############################################################################
# Copyright(c) Open Law Library. All rights reserved.                      #
# See ThirdPartyNotices.txt in the project root for additional notices.    #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License")           #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http: // www.apache.org/licenses/LICENSE-2.0                         #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################
import json

import pytest
from mock import Mock
from pygls.types import (DidCloseTextDocumentParams, DidOpenTextDocumentParams,
                         TextDocumentIdentifier, TextDocumentItem)
from pygls.workspace import Document, Workspace

from ...server import completions, did_close, did_open


class FakeServer():
    """We don't need real server to unit test features."""

    def __init__(self):
        self.workspace = Workspace('', None)


fake_document_uri = 'file://fake_doc.txt'
fake_document_content = 'text'
fake_document = Document(fake_document_uri, fake_document_content)


server = FakeServer()
server.publish_diagnostics = Mock()
server.show_message = Mock()
server.show_message_log = Mock()
server.workspace.get_document = Mock(return_value=fake_document)


def _reset_mocks():
    server.publish_diagnostics.reset_mock()
    server.show_message.reset_mock()
    server.show_message_log.reset_mock()


def test_completions():
    completion_list = completions()
    labels = [i.label for i in completion_list.items]

    assert '"' in labels
    assert '[' in labels
    assert ']' in labels
    assert '{' in labels
    assert '}' in labels


def test_did_close():
    _reset_mocks()

    params = DidCloseTextDocumentParams(
        TextDocumentIdentifier(fake_document_uri))

    did_close(server, params)

    # Check if show message is called
    server.show_message.assert_called_once()


@pytest.mark.asyncio
async def test_did_open():
    _reset_mocks()

    expected_msg = None

    # Get expected error message
    try:
        json.loads(fake_document_content)
    except json.JSONDecodeError as err:
        expected_msg = err.msg

    params = DidOpenTextDocumentParams(
        TextDocumentItem(fake_document_uri, 'json', 1, fake_document_content))

    await did_open(server, params)

    # Check publish diagnostics is called
    server.publish_diagnostics.assert_called_once()

    # Check publish diagnostics args message
    args = server.publish_diagnostics.call_args
    assert args[0][1][0].message is expected_msg

    # Check other methods are called
    server.show_message.assert_called_once()
    server.show_message_log.assert_called_once()
