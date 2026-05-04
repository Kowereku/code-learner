module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "scope-empty": [2, "never"],
    "scope-case": [0],
    "scope-pattern": [2, "always", /^[A-Z][A-Z0-9]+-\d+$/],
  },
};
