import prettier from "eslint-config-prettier";
import html from "@html-eslint/eslint-plugin";
import perfectionist from "eslint-plugin-perfectionist";

export default [
  perfectionist.configs["recommended-natural"],
  {
    ...html.configs["flat/recommended"],
    files: ["**/*.html"],
    rules:{
      "@html-eslint/indent": ["error", 2]
    }
  },
  prettier,
];
