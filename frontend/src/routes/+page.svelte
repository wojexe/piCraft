<script lang="ts">
  import type { PageData } from "./$types";

  import Intro from "../components/intro.svelte";
  import Handler from "../components/handler.svelte";

  export let data: PageData;

  const { acceptedFileTypes, availableModifications } = data;
</script>

<Intro />
<Handler {acceptedFileTypes} {availableModifications} />
