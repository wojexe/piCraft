<script lang="ts">
  import { writable, type Writable } from "svelte/store";

  import {
    acceptedFileTypes,
    availableModifications as availableModifs,
    modificationParams as modifParams,
    type AvailableModifications,
    type Modification
  } from "$lib/api";

  import InputParams from "./form/input_params.svelte";
  import CommittedModifications from "./form/committed_modifications.svelte";

  let selectedModifID = availableModifs[0].id;
  let selectedParams = structuredClone(modifParams[selectedModifID]);

  const selectModif = (id: AvailableModifications) => {
    selectedParams = structuredClone(modifParams[id]);
  };

  let commitedModifications: Writable<Array<Modification>> = writable([]);

  const commitModif = () => {
    const mod: Modification = {
      ...(availableModifs.find((mod) => mod.id === selectedModifID) as any),
      params: selectedParams
    };

    commitedModifications.update((val) => {
      val.push(mod);
      return val;
    });

    selectedModifID = availableModifs[0].id;
    selectedParams = structuredClone(modifParams[selectedModifID]);
  };

  const submitForm = () => {
    console.log("submitForm");

    if ($commitedModifications.length === 0) {
      // TODO: tost the user to select an modification and do nothing

      console.log("no modifs");

      return;
    }

    if ($commitedModifications.length === 1) {
      // TODO: perfom a singular request from a modification

      console.log("single modif");

      return;
    }

    console.log("combined modifs");
  };
</script>

<form class="handler" on:submit|preventDefault={() => submitForm()}>
  <div class="frag">
    <label for="file-picker" class="subsection">Select your image:</label>
    <input id="file-picker" type="file" required accept={acceptedFileTypes.join(",.")} />
  </div>

  <div class="frag">
    <label for="select-modification" class="subsection">Choose modifications:</label>
    <select
      id="select-modification"
      bind:value={selectedModifID}
      on:change={() => selectModif(selectedModifID)}
    >
      {#each availableModifs as modif}
        <option value={modif.id}>{modif.display}</option>
      {/each}
    </select>

    <InputParams params={selectedParams} />

    {#if $commitedModifications.length < 4}
      <input type="button" value="+" on:click={() => commitModif()} />
    {:else}
      <span class="reachedLimit">You can pick atmost 4 modification at a time!</span>
    {/if}
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

    .reachedLimit {
      font-weight: 500;
      margin-top: 0.25rem;
    }
  }
</style>
