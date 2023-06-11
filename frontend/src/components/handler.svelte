<script lang="ts">
  import { PiCraftAPI } from "$lib/api";
  import { tick } from "svelte";

  const acceptedFileTypes = PiCraftAPI.acceptedFileTypes;
  const availableModifications = PiCraftAPI.availableModifications;

  let selectedModification: PiCraftAPI.Modification | null = availableModifications[0];

  let commitedModitications: Array<PiCraftAPI.Modification> = [];

  $: console.log(commitedModitications);

  const addModification = async () => {
    if (selectedModification == null) return;

    commitedModitications.push(selectedModification);
    commitedModitications = commitedModitications; // Trigger change

    // Reset the inputs
    selectedModification = null;
    await tick();
    selectedModification = availableModifications[0];
  };
</script>

<form class="handler">
  <!-- TODO: Implement a custom-styled file input button (show filename) -->
  <!-- https://jsfiddle.net/4cwpLvae/ -->
  <div class="frag">
    <label for="file-picker" class="subsection">Select your image:</label>
    <input id="file-picker" type="file" accept={acceptedFileTypes.join(",")} />
  </div>

  <div class="frag">
    <label for="select-modification" class="subsection">Choose modifications:</label>
    <select id="select-modification" bind:value={selectedModification}>
      {#each availableModifications as modif}
        <option value={modif}>{modif.display}</option>
      {/each}
    </select>
    {#if selectedModification != null && selectedModification.params.length > 0}
      <div class="modificationParams">
        {#each selectedModification?.params as param}
          <div class="modificationParam">
            <label for={`param${param.name}`}>{param.display}</label>
            <input id={`param${param.name}`} type={param.type} />
          </div>
        {/each}
      </div>
    {/if}

    <input type="button" value="+" on:click|preventDefault={() => addModification()} />
  </div>

  <div class="frag">
    <span class="subsection">Selected modifications:</span>
    {#each commitedModitications as modif}
      {modif.display}<br />
    {/each}
  </div>

  <input id="submit-form" type="submit" value="Process image" />
</form>

<style lang="scss">
  .handler {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    padding: 2em;

    border-radius: 2em;

    background-color: var(--card-background);

    .frag {
      display: flex;
      flex-direction: column;
      place-items: center;
      gap: 0.5rem;

      width: 100%;
    }

    .subsection {
      align-self: flex-start;
      font-size: 1.2em;
      font-weight: 500;
      margin-bottom: 0.5rem;
    }

    .modificationParams {
      display: flex;
      flex-direction: row;
      width: 100%;
      justify-content: space-around;
      gap: 1rem;

      .modificationParam {
        display: flex;
        flex-direction: column;
        label {
          font-size: 0.8em;
          font-weight: 500;
        }
        input {
          width: 12ch;
          padding: 0.5ch 1ch;
          border: none;

          border-radius: 1rem;
        }
      }
    }
  }
</style>
