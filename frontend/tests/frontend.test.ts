import { expect, test } from "@playwright/test";

test("Should not allow submitting with no modifications", async ({ page }) => {
  await page.goto("/");

  await page.setInputFiles("#file-picker", "./tests/rollo.jpg");

  // No modification chosen

  const submitButton = await page.$("#submit-form");
  expect(submitButton).toBeNull();

  const noModifsTextLocator = page.getByText("No modifications selected yet!", { exact: true });
  expect(noModifsTextLocator).not.toBeNull();
});

test("Should not allow submitting with no file", async ({ page }) => {
  await page.goto("/");

  // No file chosen

  await page.click("input[type='button'][value='+']");

  const submitButton = await page.$("#submit-form");
  expect(submitButton).toBeNull();
});
