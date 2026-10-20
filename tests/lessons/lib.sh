# Shared helpers for lesson command checks, for bash and zsh.
# Source this file from a lesson script; do not run it directly.
#
# Every check runs inside a fresh temporary folder. HOME is pointed at a
# fake home folder inside it, so `cd ~` never reaches the real home folder.
# The temporary folder is removed when the script exits, also on failure.

LESSON_FAILURES=0

lesson_base=${TMPDIR:-/tmp}
LESSON_TMP=$(mktemp -d "${lesson_base%/}/lesson-check.XXXXXX") || {
    printf 'FAIL could not create a temporary folder\n'
    exit 1
}
case "$LESSON_TMP" in
    */lesson-check.??????) ;;
    *) printf 'FAIL unexpected temporary folder: %s\n' "$LESSON_TMP"; exit 1 ;;
esac

lesson_cleanup() {
    cd / && rm -rf -- "$LESSON_TMP"
}
trap lesson_cleanup EXIT

# new_home NAME: create a fake home folder, point HOME at it and go there.
# HOME is taken from `pwd`, so later comparisons with `pwd` use the same spelling.
new_home() {
    mkdir -p "$LESSON_TMP/$1/home" && cd "$LESSON_TMP/$1/home" || exit 1
    HOME=$(pwd)
    export HOME
}

# listing [PATH]: what `ls -F` shows, sorted and joined with spaces.
listing() {
    ls -F "$@" 2>/dev/null | LC_ALL=C sort | tr '\n' ' ' | sed 's/ $//'
}

pass() { printf 'ok   %s\n' "$1"; }
fail() {
    printf 'FAIL %s\n' "$1"
    shift
    for line in "$@"; do printf '     %s\n' "$line"; done
    LESSON_FAILURES=$((LESSON_FAILURES + 1))
}

# expect_eq DESCRIPTION EXPECTED ACTUAL
expect_eq() {
    if [ "$2" = "$3" ]; then pass "$1"; else fail "$1" "expected: $2" "actual:   $3"; fi
}

# expect_ok DESCRIPTION COMMAND [ARGS...]: the command succeeds (runs in this shell).
expect_ok() {
    desc=$1; shift
    if "$@" >/dev/null 2>&1; then pass "$desc"; else fail "$desc" "command failed: $*"; fi
}

# expect_fail DESCRIPTION COMMAND [ARGS...]: the command reports an error.
expect_fail() {
    desc=$1; shift
    if "$@" >/dev/null 2>&1; then fail "$desc" "command unexpectedly succeeded: $*"; else pass "$desc"; fi
}

# finish NAME: print the summary and exit with the right status.
finish() {
    if [ "$LESSON_FAILURES" -eq 0 ]; then
        printf 'PASSED %s\n' "$1"
        exit 0
    fi
    printf 'FAILED %s: %s check(s) failed\n' "$1" "$LESSON_FAILURES"
    exit 1
}
