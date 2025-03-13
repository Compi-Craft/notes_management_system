<template>
  <div id="app">
    <h1>Notes Analytics</h1>

    <div v-if="loading" class="loading">
      <p>Loading data...</p>
    </div>

    <div v-else>
      <div class="analytics">
        <h2>Total Word Count</h2>
        <p>{{ analytics.total_word_count }}</p>

        <h2>Average Note Length</h2>
        <p>{{ analytics.average_note_length }} words</p>

        <h2>Most Common Words</h2>
        <ul>
          <li v-for="(word, index) in analytics.most_common_words" :key="index">
            {{ word[0] }}: {{ word[1] }} times
          </li>
        </ul>

        <h2>Top 3 Longest Notes</h2>
        <ul>
          <li v-for="(note, index) in analytics.top_3_longest_notes" :key="index">
            {{ note.title }} - {{ note.content_length }} characters
          </li>
        </ul>

        <h2>Top 3 Shortest Notes</h2>
        <ul>
          <li v-for="(note, index) in analytics.top_3_shortest_notes" :key="index">
            {{ note.title }} - {{ note.content_length }} characters
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
<script src="./assets/js/App.js"></script>
<style src="./assets/styles/App.css"></style>
