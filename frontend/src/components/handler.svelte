<script lang="ts">
  import { writable, type Writable } from "svelte/store";

  import {
    acceptedFileTypes,
    availableModifications as availableModifs,
    modificationParams as modifParams,
    type AvailableModifications,
    type Modification,
    modificationFetch
  } from "$lib/api";

  import InputParams from "./form/input_params.svelte";
  import CommittedModifications from "./form/committed_modifications.svelte";

  let files: FileList;
  const selected = {
    modifID: availableModifs[0].id,
    params: structuredClone(modifParams[availableModifs[0].id])
  };
  let commitedModifications: Writable<Array<Modification>> = writable([]);

  const clearModifs = () => {
    selected.modifID = availableModifs[0].id;
    selected.params = structuredClone(modifParams[selected.modifID]);
  };

  const clearSubmitted = () => {
    commitedModifications.set([]);
  };

  const selectModif = (id: AvailableModifications) => {
    selected.params = structuredClone(modifParams[id]);
  };

  const commitModif = () => {
    const mod: Modification = {
      ...(availableModifs.find((mod) => mod.id === selected.modifID) as any),
      params: selected.params
    };

    commitedModifications.update((val) => {
      val.push(mod);
      return val;
    });

    clearModifs();
  };

  const submitForm = async () => {
    if ($commitedModifications.length === 0) {
      // this branch should never happen in fact
      // TODO: tost the user to select an modification and do nothing

      console.log("no modifs");

      return;
    }

    try {
      const response = await modificationFetch(files[0], $commitedModifications);

      if (response.ok) {
        const blob = await response.blob();
        window.open(URL.createObjectURL(blob));
      } else {
        // show error with toast
        const json = await response.json();

        console.error(json);
      }
    } catch (e) {
      // handle this error as well

      console.log("rejection", e);
    }

    clearModifs();
    clearSubmitted();
  };
</script>

<form class="handler" on:submit|preventDefault={async () => await submitForm()}>
  <div class="frag">
    <label for="file-picker" class="subsection">Select your image:</label>
    <input id="file-picker" type="file" bind:files required accept={acceptedFileTypes.join(",.")} />
  </div>

  <div class="frag">
    <label for="select-modification" class="subsection">Choose modifications:</label>
    <select
      id="select-modification"
      bind:value={selected.modifID}
      on:change={() => selectModif(selected.modifID)}
    >
      {#each availableModifs as modif}
        <option value={modif.id}>{modif.display}</option>
      {/each}
    </select>

    <InputParams params={selected.params} />

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

  {#if files != null && $commitedModifications.length !== 0}
    <input id="submit-form" type="submit" value="Process image" />
  {/if}
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
