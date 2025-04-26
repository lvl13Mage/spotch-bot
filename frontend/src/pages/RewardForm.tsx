import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { useTheme } from "@/components/ThemeProvider"; // Import the useTheme hook

const RewardForm = () => {
  const { id } = useParams<{ id: string }>(); // Retrieve id from route parameters
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [type, setType] = useState("");
  const [amount, setAmount] = useState(0);
  const [active, setActive] = useState(false);
  const [types, setTypes] = useState<{ technical_label: string; user_label: string }[]>([]);
  const [usedRewardTypes, setUsedRewardTypes] = useState<string[]>([]); // Track used reward types
  const [loading, setLoading] = useState(true); // Loading state for fetching data
  const [saving, setSaving] = useState(false); // Saving state for form submission
  const navigate = useNavigate(); // Use navigate for redirection
  const { theme } = useTheme(); // Access the current theme (e.g., "light", "dark", "system")

  const fetchReward = async () => {
    if (id) {
      try {
        const response = await axios.get(`/twitch/rewards/${id}`);
        const reward = response.data;
        setName(reward.name);
        setDescription(reward.description);
        setType(reward.type);
        setAmount(reward.amount);
        setActive(reward.active);
      } catch (error) {
        console.error("Failed to fetch reward:", error);
        alert("Failed to fetch reward details.");
      }
    }
  };

  const fetchTypes = async () => {
    try {
      const response = await axios.get("/twitch/rewards/types");
      setTypes(response.data); // Populate the dropdown
    } catch (error) {
      console.error("Failed to fetch reward types:", error);
      alert("Failed to fetch reward types.");
    }
  };

  const fetchUsedRewardTypes = async () => {
    try {
      const response = await axios.get("/twitch/rewards?active_only=false"); // Fetch all rewards
      const rewards = response.data;

      // Exclude the type of the reward being edited (if in edit mode)
      const usedTypes = rewards
        .filter((reward: { id: string }) => reward.id !== id) // Exclude the current reward
        .map((reward: { type: string }) => reward.type); // Extract used types

      setUsedRewardTypes(usedTypes);
    } catch (error) {
      console.error("Failed to fetch used reward types:", error);
      alert("Failed to fetch used reward types.");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true); // Set saving state
    const payload = { name, description, type, amount, active };
    console.log("Submitting payload:", payload); // Log the payload for debugging
    try {
      if (id) {
        await axios.patch(`/twitch/rewards/${id}`, payload); // Updated to PATCH
      } else {
        await axios.post("/twitch/rewards", payload); // Updated to POST
      }
      navigate("/rewards");
    } catch (error) {
      console.error("Failed to save reward:", error);
      alert("Failed to save reward. Please try again.");
    } finally {
      setSaving(false); // Reset saving state
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true); // Set loading state
      await fetchTypes();
      await fetchUsedRewardTypes();
      await fetchReward();
      setLoading(false); // Reset loading state
    };
    fetchData();
  }, [id]);

  if (loading) {
    return <div>Loading...</div>; // Show loading indicator while fetching data
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">{id ? "Edit Reward" : "Add Reward"}</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm">Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full border p-2"
            required
          />
        </div>
        <div>
          <label className="block text-sm">Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full border p-2"
            required
          />
        </div>
        <div>
          <label className="block text-sm">Type</label>
          <select
            value={type}
            onChange={(e) => setType(e.target.value)}
            className={`w-full border p-2 rounded focus:outline-none focus:ring-2 ${
              theme === "dark"
                ? "bg-purple-900 text-purple-100 border-purple-600 focus:ring-purple-500"
                : "bg-purple-100 text-purple-900 border-purple-300 focus:ring-purple-500"
            }`}
            required
          >
            <option value="" disabled>
              Select a type
            </option>
            {types
              .filter(
                (rewardType) =>
                  !usedRewardTypes.includes(rewardType.technical_label) || rewardType.technical_label === type
              ) // Show unused types or the current type if editing
              .map((rewardType) => (
                <option key={rewardType.technical_label} value={rewardType.technical_label}>
                  {rewardType.user_label}
                </option>
              ))}
          </select>
        </div>
        <div>
          <label className="block text-sm">Cost</label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(Number(e.target.value))}
            className="w-full border p-2"
            required
            min={0}
          />
        </div>
        <div>
          <label className="block text-sm">Active</label>
          <input
            type="checkbox"
            checked={active}
            onChange={(e) => setActive(e.target.checked)}
          />
        </div>
        <div className="flex justify-between">
          <button
            type="submit"
            className={`bg-blue-500 text-white px-4 py-2 ${saving ? "opacity-50 cursor-not-allowed" : ""}`}
            disabled={saving} // Disable button while saving
          >
            {saving ? "Saving..." : "Save"}
          </button>
          <button
            type="button"
            onClick={() => navigate("/rewards")} // Navigate back to the rewards list
            className="bg-gray-500 text-white px-4 py-2"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default RewardForm;