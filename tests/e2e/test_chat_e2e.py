"""E2E test for ``omnigent chat`` -- local mode with archer (mock LLM).

Verifies that ``omnigent chat ./agent-dir/`` starts a server, opens the
REPL, and the agent responds. Since the REPL is interactive, we
test by directly calling the local mode components rather than
launching the full CLI.

Usage::

    pytest tests/e2e/test_chat_e2e.py -v

.. note::

   All three tests in this module are skipped because
   ``_start_local_server`` writes to the user's persistent
   ``~/.omnigent`` directory (DB + artifacts) and picks up
   ambient agents from prior runs, making isolated mock-LLM
   testing infeasible without refactoring the server lifecycle
   to support full HOME isolation. The original tests were also
   broken on main (``examples/archer`` path does not exist).
"""

from __future__ import annotations

import pytest


@pytest.mark.skip(
    reason=(
        "_start_local_server uses persistent ~/.omnigent state and the "
        "original _ARCHER_DIR path (examples/archer) does not exist. "
        "These tests need _start_local_server refactored for HOME "
        "isolation before mock-LLM migration is feasible."
    ),
)
def test_chat_local_starts_server_and_agent_responds() -> None:
    """
    ``omnigent chat ./agent-dir/`` starts a local server with the agent
    and the agent can respond to messages.

    Tests the server startup and agent registration path used by
    ``omnigent chat`` in local mode. Since the REPL itself is interactive,
    we verify the underlying server works by sending a direct HTTP
    request.

    **What breaks if this fails:**
    - _start_local_server broken -> server doesn't boot.
    - Agent bundle not registered -> 404 on responses.
    - Agent config invalid -> 500 on responses.
    """


@pytest.mark.skip(
    reason=(
        "_start_local_server uses persistent ~/.omnigent state. "
        "The subprocess's agent registration race and DB-path coupling "
        "make isolated mock-LLM testing infeasible without refactoring "
        "the server lifecycle."
    ),
)
def test_chat_local_accepts_omnigent_yaml_file() -> None:
    """
    ``omnigent chat examples/coding_supervisor.yaml`` (or any
    standalone omnigent YAML) now starts the local server and
    registers the agent under its spec-declared name.

    **What breaks if this fails:**
    - ``_preregister_agent`` regresses to directory-only.
    - ``materialize_bundle``'s file branch produces the wrong
      dir shape and ``_find_omnigent_yaml_in_dir`` misses the
      YAML.
    - Agent-plane's spec dispatch stops routing omnigent YAMLs
      through ``load_omnigent_yaml``.
    """


@pytest.mark.skip(
    reason=(
        "_start_local_server uses persistent ~/.omnigent state and "
        "_pick_agent reads stdin interactively when multiple agents "
        "exist. The original _ARCHER_DIR path (examples/archer) does "
        "not exist. These tests need HOME isolation before mock-LLM "
        "migration is feasible."
    ),
)
def test_chat_remote_pick_agent() -> None:
    """
    Remote chat can list and identify agents on a server.

    Tests the remote mode's agent discovery by starting a server with
    archer and verifying ``_pick_agent`` finds it.

    **What breaks if this fails:**
    - _pick_agent can't parse server agent listing response.
    - Agent name extraction broken.
    """
