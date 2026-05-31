const JIRA_SCOPE_RE = /^[A-Z][A-Z0-9]+-\d+$/;

module.exports = {
  extends: ["@commitlint/config-conventional"],
  plugins: [
    {
      rules: {
        "scope-jira": ({ scope }) => [
          !scope || JIRA_SCOPE_RE.test(scope),
          "scope, when present, must be a JIRA key like ABC-123",
        ],
      },
    },
  ],
  rules: {
    "scope-empty": [0],
    "scope-case": [0],
    "scope-jira": [2, "always"],
  },
};
