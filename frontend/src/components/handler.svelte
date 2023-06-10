<script lang="ts">
  import { PiCraftAPI } from "$lib/api";

  const acceptedFileTypes = PiCraftAPI.acceptedFileTypes;
  const availableModifications = PiCraftAPI.availableModifications;
</script>

<form class="handler">
  <!-- TODO: Implement a custom-styled file input button (show filename) -->
  <!-- https://jsfiddle.net/4cwpLvae/ -->
  <input type="file" accept={acceptedFileTypes.join(",")} />

  <label for="select-operation">Choose modifications:</label>
  <select id="select-operation">
    {#each availableModifications as modif}
      <option value={modif.name}>{modif.display}</option>
    {/each}
  </select>

  <!-- TODO: A plus sign on the right of the selection -->

  <!-- TODO: A list of already chosen modifications -->

  <input type="submit" value="Process image" />
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
  }
</style>
