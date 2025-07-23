<template>
  <n-flex vertical>
  <div
  v-for="recipe in recipeList"
  :key="nanoid()"
  class="recipe-card"
  >
  <n-card>
  <n-space justify="space-between">
    <div>
  <n-h1 perfix="bar" strong align-text>
    <n-text type="primary" style="font-size: 40px">
    {{ recipe.name }}
  </n-text>
  </n-h1>
  <n-h2 perfix="bar" align-text>
    <n-text style="font-size: 30px">
    材料
  </n-text>
  </n-h2>
  <n-ul>
    <n-li v-for="(ingredient) in recipe.ingredients" :key="nanoid()"
      style="font-size: 20px">
      {{ ingredient }}
    </n-li>
  </n-ul>
  <n-h3 perfix="bar" align-text>
    <n-text style="font-size: 30px">
    做法
  </n-text>
  </n-h3>
  <n-ol>
    <n-li v-for="(step, index) in recipe.steps" :key="index"
    style="font-size: 20px">
      {{ step }}
    </n-li>
  </n-ol>
</div>
  <img 
  v-if="recipe.img"
  :src="recipe.img"
  style="width: 600px; margin-top: 50px"
  />
</n-space>
  </n-card>
  </div>
  </n-flex>
</template>

<script lang="ts"> export default {name: "About"}</script>
<script setup lang="ts">
import {nanoid} from 'nanoid';
import { onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import {NFlex, NSpace, NCard, NH1, NH2, NH3, NLi, NOl, NUl, NText} from 'naive-ui'
import { useRecipeStore } from '@/stores/recipe';

const recipeStore = useRecipeStore();
const { recipeList } = storeToRefs(recipeStore);

onMounted(async () => {
  await recipeStore.loadRecipes();
})

</script>

<style scoped>
.recipe-card {
  margin-bottom: 16px;
  margin-left: 13%;
  margin-right: 13%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>