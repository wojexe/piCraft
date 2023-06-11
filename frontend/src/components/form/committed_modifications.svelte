<script lang="ts">
  import type { PiCraftAPI } from "@/lib/api";

  export let modifications: Array<PiCraftAPI.Modification>;
</script>

{#each modifications as modif}
  {modif.display}<br />
{/each}
