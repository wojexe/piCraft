import { expect, test } from "@playwright/test";

test("Sends request properly and receives result", async ({ page, context }) => {
  await page.goto("/");

  await page.setInputFiles("#file-picker", "./tests/rollo.jpg");
  await page.click("input[type='button'][value='+']");

  const responsePromise = page.waitForResponse((resp) => resp.status() === 200);
  const pagePromise = context.waitForEvent("page");

  await page.click("#submit-form");

  await responsePromise;
  const newPage = await pagePromise;

  const img = await newPage.$("img");
  expect(img).not.toBeNull();
});
