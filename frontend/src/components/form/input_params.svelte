<script lang="ts">
  import { getContext } from "svelte";
  import type { Writable } from "svelte/store";

  import type { PiCraftAPI } from "@/lib/api";
  import ParameterInput from "./parameter_input.svelte";

  const modification: Writable<PiCraftAPI.Modification> = getContext("writableModification");

  const hasParams = (mod: PiCraftAPI.Modification) => mod.params.length > 0;
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
