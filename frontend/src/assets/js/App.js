import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      analytics: null,
      loading: true,
    };
  },
  mounted() {
    this.fetchAnalyticsData();
  },
  methods: {
    async fetchAnalyticsData() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/analytics");
        this.analytics = response.data;
        this.loading = false;
      } catch (error) {
        console.error("Error fetching analytics data:", error);
        this.loading = false;
      }
    },
  },
};
