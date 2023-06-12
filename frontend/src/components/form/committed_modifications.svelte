<script lang="ts">
  import type { Modification } from "@/lib/api";

  export let modifications: Array<Modification>;

  const removeModif = (i: number) => {
    modifications.splice(i, 1);
    modifications = modifications;
  };
</script>

{#if modifications.length > 0}
  <div class="modifications">
    {#each modifications as modif, i}
      <div class="modification-wrapper">
        <div class="modification">
          <span class="modification-name">{modif.display}</span>
          {#if modif.params.length > 0}
            <div class="modification-params">
              {#each modif.params as param}
                <span>{param.display}: {param.value ?? param.defaultValue}</span>
              {/each}
            </div>
          {/if}
        </div>
        <span class="remove-button" on:click={() => removeModif(i)}>❌</span>
      </div>
    {/each}
  </div>
{:else}
  No modifications selected yet!
{/if}

<style lang="scss">
  .modifications {
    display: flex;
    width: 90%;
    flex-direction: column;
    gap: 2rem;
    padding: 1em;

    border-radius: 1em;
    background-color: var(--card-background--light);

    .modification-wrapper {
      position: relative;
      display: flex;
      width: 100%;
      flex-direction: row;
      justify-content: space-between;
      align-items: center;

      &::after {
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translate(-50%, 1rem);
        content: " ";

        width: 16ch;
        height: 2px;
        background-color: rgba(255, 255, 255, 0.1);
      }

      &:last-of-type::after {
        display: none;
      }
    }

    .modification {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .modification-params {
      display: flex;
      flex-direction: row;
      font-size: 0.8em;
      gap: 1.5ch;

      span {
        position: relative;

        &:last-of-type {
          &::after {
            display: none;
          }
        }

        &::after {
          position: absolute;
          content: " ";
          top: 50%;
          right: 0;

          width: 0.5ch;
          height: 0.5ch;

          transform: translate(1ch, -50%);

          background-color: rgba(255, 255, 255, 0.3);
          border-radius: 1ch;
        }
      }
    }

    .modification-name {
      font-weight: 500;
    }

    .remove-button {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 1ch;
      height: 1ch;
      padding: 0.75em;
      background-color: rgba(255, 255, 255, 0.1);
      border-radius: 2em;
      cursor: pointer;

      transition: background-color ease-in-out 0.1s;
      &:hover {
        background-color: rgba(255, 255, 255, 0.25);
      }
    }
  }
</style>
