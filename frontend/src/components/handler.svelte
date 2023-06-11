<script lang="ts">
  import { PiCraftAPI } from "$lib/api";
  import { setContext } from "svelte";

  import InputParams from "./form/input_params.svelte";
  import CommittedModifications from "./form/committed_modifications.svelte";
  import { writable, type Writable } from "svelte/store";

  const acceptedFileTypes = PiCraftAPI.acceptedFileTypes;
  const availableModifications = PiCraftAPI.availableModifications;

  let selectedModification: PiCraftAPI.Modification = availableModifications[0];

  const writableModification: Writable<PiCraftAPI.Modification> = writable(
    structuredClone(selectedModification)
  );

  const selectModification = (val: PiCraftAPI.Modification) => {
    writableModification.set(structuredClone(val));
  };

  setContext("writableModification", writableModification);

  let commitedModifications: Array<PiCraftAPI.Modification> = [];

  const commitModification = () => {
    writableModification.update((val) => {
      commitedModifications.push(val);
      commitedModifications = commitedModifications; // Trigger update

      return structuredClone(availableModifications[0]);
    });
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
    <select
      id="select-modification"
      bind:value={selectedModification}
      on:change={() => selectModification(selectedModification)}
    >
      {#each availableModifications as modif}
        <option value={modif}>{modif.display}</option>
      {/each}
    </select>

    <InputParams />

    <input type="button" value="+" on:click|preventDefault={() => commitModification()} />
  </div>

  <div class="frag">
    <span class="subsection">Selected modifications:</span>
    <CommittedModifications modifications={commitedModifications} />
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
  }
</style>
