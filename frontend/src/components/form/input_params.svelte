<script lang="ts">
  import ParameterInput from "./parameter_input.svelte";

  export let params: Array<any>;
</script>

{#if params.length > 0}
  <div class="modificationParams">
    {#each params as param}
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
