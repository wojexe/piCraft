import type { PageLoad } from './$types';
import {acceptedFileTypes, availableModifications} from "../shared/available.json";

export const load = (() => {
  // const acceptedFileTypes: Array<string> = available.acceptedFileTypes;
  // const availableModifications: Array<string> = available.availableModifications;

  return {
    acceptedFileTypes,
    availableModifications
  };
}) satisfies PageLoad;
