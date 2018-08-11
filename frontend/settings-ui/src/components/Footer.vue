<template>
	<div>
		<footer class="footer navbar-light bg-light">
			<span>Developed by Silence & Befezdow 2k18</span>
		</footer>
	</div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';

	@Component
	export default class Footer extends Vue {}
</script>

<style scoped>
	.footer {
		text-align: center;
		padding-top: 15px;
		padding-bottom: 15px;
	}
</style>