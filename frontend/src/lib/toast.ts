import { toast } from "@zerodevx/svelte-toast";

const errorOptions = {
  theme: {
    "--toastColor": "white",
    "--toastBackground": "crimson",
    "--toastBarBackground": "darkred"
  }
};

export const errorToast = (msg: string) => toast.push(msg, errorOptions);
