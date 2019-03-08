<template>
    <div class="col-lg-2 padding-top-xs">
        <div>
            <b-progress :value="percentValue" :variant="percentValue | variantType" :style="{background: backgroundColor}"/>
        </div>
        <div align="center" style="font-size: smaller">
            {{bytesToHumanMeasure(freeValue)}} свободно из {{bytesToHumanMeasure(maxValue)}}
        </div>
    </div>
</template>

<script>
export default {
    name: 'CapacityComponent',
    props: {
        percentValue: {
            type: Number,
            required: true
        },
        freeValue: {
            type: Number,
            required: true
        },
        maxValue: {
            type: Number,
            required: true
        },
        floatPrecision: {
            type: Number,
            default: 1
        },
        backgroundColor: {
            type: String,
            default: '#cbcbcb'
        }
    },
    methods: {
        // this is not a filter because this context is needed
        bytesToHumanMeasure(value) {
            if (!value) return ''

            let result = parseInt(value);
            let multiplicity = 0;
            while (true) {
                result = result / 1024;
                multiplicity++;
                if (result < 1024 || multiplicity >= 4) {
                    break;
                }
            }
            result = result.toFixed(this.floatPrecision).toString();
            switch (multiplicity) {
                case 0:
                    result = `${result} б`;
                    break;
                case 1:
                    result = `${result} Кб`;
                    break;
                case 2:
                    result = `${result} Мб`;
                    break;
                case 3:
                    result = `${result} Гб`;
                    break;
                case 4:
                    result = `${result} Тб`;
                    break;
            }
            return result;
        }
    },
    filters: {
        variantType(percentValue) {
            if (percentValue > 80) {
                return 'danger';
            } else if (percentValue > 60) {
                return 'warning';
            } else if (percentValue > 40) {
                return 'info';
            } else {
                return 'success';
            }
        }
    }
}
</script>

<style scoped>

</style>
