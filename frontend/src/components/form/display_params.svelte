<script lang="ts">
  import { getContext } from "svelte";
  import type { Writable } from "svelte/store";

  import type { Modification } from "@/lib/api";
  import ParameterInput from "./parameter_input.svelte";

  const modification: Writable<Modification> = getContext("writableModification");

  const hasParams = (mod: Modification) => mod.params.length > 0;
</script>

{#if hasParams($modification)}
  <div class="modificationParams">
    {#each $modification?.params as param}
      <ParameterInput {param} />
    {/each}
  </div>
{/if}

<style lang="scss">
  .modificationParams {
    display: flex;
    flex-direction: row;
    width: 100%;
    justify-content: space-around;
    gap: 1rem;
  }
</style>
