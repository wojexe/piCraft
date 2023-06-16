<script lang="ts">
</script>

<div class="intro">
  <h2 class="title">Your go-to image processor</h2>
  <p class="description">
    Upload an image using the form below and choose any of the listed options to create the picture
    you want!
  </p>
</div>

<style lang="scss">
  .intro {
    display: flex;
    flex-direction: column;
    place-items: center;
    gap: 1em;

    max-width: 36ch;
    padding: 2em;

    border-radius: 2em;
    background-color: var(--card-background);

    & .title {
      margin: 0;
      font-weight: 500;
    }

    & .description {
      margin: 0;
    }
  }
</style>
