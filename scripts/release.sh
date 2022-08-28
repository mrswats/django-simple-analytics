#!/bin/bash

help() {
	echo "Usage:"
	echo "  $0 <rule> <options>"
	echo "  rule: major | minor | patch"
	echo "  options:"
	echo "    --force create a release commit even if repo is dirty"
	echo "    --push push release commit with tags"
}

check-if-in-virtualenv() {
	if [[ -n $VIRTUAL_ENV ]]; then
		return 0
	fi

	echo "Not in a virtualenv!"
	return 1
}

check-if-repo-is-dirty() {
	git diff-index --quiet HEAD -- && return 0
}

bump-version() {
	local rule
	rule=$1
	poetry version "$rule"
}

create-release-commit() {
	local version
	version=$(poetry version --short)
	git add pyproject.toml
	SKIP=no-commit-to-branch git commit -m "Release ${version}"
	git tag "v${version}" -m "Release ${version}"
}

push-tags() {
	git push --follow-tags
}

parse-opts() {
	while [[ "$#" -gt 0 ]]; do
		case "$1" in
		--force)
			FORCE_PUSH='true'
			shift
			;;
		--push)
			PUSH_TAGS='true'
			shift
			;;
		--help)
			help
			exit 0
			shift
			;;
		*)
			shift
			;;
		esac
	done
}

parse-rule() {
	case "$1" in
	major | minor | patch)
		RULE="$1"
		;;
	*)
		echo "Unkown rule '$1'"
		echo "Accepted rules: major, minor, patch"
		help
		exit 1
		;;
	esac
}

main() {
	check-if-in-virtualenv || exit 1

	parse-opts "$@"
	parse-rule "$@"

	if [[ ! ${FORCE_PUSH} ]]; then
		if [[ $(check-if-repo-is-dirty) ]]; then
			echo "Repo is dirty. Can't release in this state"
			echo " use '--force' to override this behaviour"
			exit 1
		fi
	fi

	bump-version "$RULE"
	create-release-commit

	if [[ ${PUSH_TAGS} ]]; then
		push-tags
	else
		echo "All left to do is to"
		echo "\$ git push --follow-tags"
		echo "  use '--push' to directly push the newly created tags"
	fi
}

main "$@"
