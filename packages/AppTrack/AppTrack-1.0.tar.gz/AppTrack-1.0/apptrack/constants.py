from __future__ import absolute_import, unicode_literals, print_function

from . import __version__

import six

# Max number of bits to use when generating random ID
MAX_ID_BITS = 64

# How often remotely controller sampler polls for sampling strategy
DEFAULT_SAMPLING_INTERVAL = 60

# How often remote reporter does a preemptive flush of its buffers
DEFAULT_FLUSH_INTERVAL = 1

# Name of the HTTP header used to encode trace ID
TRACE_ID_HEADER = 'apptrack-trace-id' if six.PY3 else b'apptrack-trace-id'

# Prefix for HTTP headers used to record baggage items
BAGGAGE_HEADER_PREFIX = 'apptrackctx-' if six.PY3 else b'apptrackctx-'

# The name of HTTP header or a TextMap carrier key which, if found in the
# carrier, forces the trace to be sampled as "debug" trace. The value of the
# header is recorded as the tag on the # root span, so that the trace can
# be found in the UI using this value as a correlation ID.
DEBUG_ID_HEADER_KEY = 'apptrack-debug-id'

APPTRACK_CLIENT_VERSION = 'Python2-v%s' % __version__

# Tracer-scoped tag that tells the version of Algo client library
APPTRACK_VERSION_TAG_KEY = 'apptrack.version'

# Tracer-scoped tag that contains the hostname
APPTRACK_HOSTNAME_TAG_KEY = 'apptrack.hostname'

APPTRACK_IPV4_TAG_KEY = 'apptrack.ip_v4'

# the type of sampler that always makes the same decision.
SAMPLER_TYPE_CONST = 'const'

# the type of sampler that polls Algo agent for sampling strategy.
SAMPLER_TYPE_REMOTE = 'remote'

# the type of sampler that samples traces with a certain fixed probability.
SAMPLER_TYPE_PROBABILISTIC = 'probabilistic'

# the type of sampler that samples only up to a fixed number
# of traces per second.
# noinspection SpellCheckingInspection
SAMPLER_TYPE_RATE_LIMITING = 'ratelimiting'

# the type of sampler that samples only up to a fixed number
# of traces per second.
# noinspection SpellCheckingInspection
SAMPLER_TYPE_LOWER_BOUND = 'lowerbound'

# max length for tag values. Longer values will be truncated.
MAX_TAG_VALUE_LENGTH = 1024

# Constant for sampled flag
SAMPLED_FLAG = 0x01

# Constant for debug flag
DEBUG_FLAG = 0x02


DATABASE_HOST_KEY = 'db.host'

DATABASE_PORT_KEY= 'db.port'

GEN_ID_RANGE = 999999

# ---------------------------------------------------------------------------
# Genetalks Cloud
# ---------------------------------------------------------------------------

USER_TOKEN = 'user_token'
PUBLIC_KEY_FOR_TOKEN = 'public_key_for_token'
PROCESS_ID = 'process_id'
PROCESS_ARGS = 'process_args'

SPAN_ID = 'span_id'
START_TIME = 'start_time'
FINISH_TIME = 'finish_time'
FINISH_INFO = 'finish_info'
FINISH_STATUS = 'finish_status'
FINISH_REASON = 'finish_reason'

CHILDREN_DIR = 'children'
CHILDREN_NUM_ALLOCATOR = "children_num_allocator"

FINISH_STATUS_SUCC = "ok"
FINISH_STATUS_FAILED = "failed"
FINISH_STATUS_RETRY = "retry"


NOOP_SPAN_ID = 'span_noop'

FINISH_RESULT = 'finish_result'  # this tags's value must be { bool is_success, string result_info}

