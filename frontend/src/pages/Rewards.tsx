import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEdit, faTrash, faToggleOn, faToggleOff, faPlus } from "@fortawesome/free-solid-svg-icons";

const Rewards = () => {
  interface Reward {
    id: number;
    name: string;
    amount: number;
    active: boolean;
    type: string; // Technical label of the reward type
  }

  interface RewardType {
    technical_label: string;
    user_label: string;
  }

  const [rewards, setRewards] = useState<Reward[]>([]);
  const [rewardTypes, setRewardTypes] = useState<RewardType[]>([]); // All available reward types
  const [usedRewardTypes, setUsedRewardTypes] = useState<string[]>([]); // Used reward types (technical labels)
  const [loading, setLoading] = useState(true);
  const [actionInProgress, setActionInProgress] = useState(false); // Track ongoing actions
  const navigate = useNavigate();

  const fetchRewards = async () => {
    setLoading(true);
    try {
      const response = await axios.get("/twitch/rewards?active_only=false"); // Updated route
      setRewards(response.data);
      setUsedRewardTypes(response.data.map((reward: Reward) => reward.type)); // Extract used reward types
    } catch (error) {
      console.error("Failed to fetch rewards:", error);
      alert("Failed to fetch rewards. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const fetchRewardTypes = async () => {
    try {
      const response = await axios.get("/twitch/rewards/types");
      setRewardTypes(response.data); // Store both technical and user labels
    } catch (error) {
      console.error("Failed to fetch reward types:", error);
      alert("Failed to fetch reward types.");
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      await fetchRewardTypes();
      await fetchRewards();
    };
    fetchData();
  }, []);

  const availableRewardTypes = rewardTypes
    .map((type) => type.technical_label)
    .filter((type) => !usedRewardTypes.includes(type)); // Calculate available types

  const getUserLabel = (technicalLabel: string) => {
    const rewardType = rewardTypes.find((type) => type.technical_label === technicalLabel);
    return rewardType ? rewardType.user_label : technicalLabel; // Fallback to technical label if not found
  };

  const syncRewards = async () => {
    try {
      await axios.post("/twitch/rewards/sync"); // Call the sync endpoint
      console.log("Rewards synced successfully.");
    } catch (error) {
      console.error("Failed to sync rewards:", error);
      alert("Failed to sync rewards. Please try again.");
    }
  };

  const deleteReward = async (id: number) => {
    if (!window.confirm("Are you sure you want to delete this reward?")) return;
    setActionInProgress(true);
    try {
      await axios.delete(`/twitch/rewards/${id}`); // Delete the reward
      setRewards((prevRewards) => prevRewards.filter((reward) => reward.id !== id));
      setUsedRewardTypes((prevTypes) => prevTypes.filter((type) => type !== rewards.find((r) => r.id === id)?.type));
      await syncRewards(); // Sync rewards after deletion
    } catch (error) {
      console.error("Failed to delete reward:", error);
      alert("Failed to delete reward. Please try again.");
    } finally {
      setActionInProgress(false);
    }
  };

  const toggleReward = async (id: number, currentState: boolean) => {
    setActionInProgress(true);
    try {
      await axios.patch(`/twitch/rewards/${id}`, { active: !currentState }); // Toggle the reward's active state
      setRewards((prevRewards) =>
        prevRewards.map((reward) =>
          reward.id === id ? { ...reward, active: !currentState } : reward
        )
      );
      await syncRewards(); // Sync rewards after toggling
    } catch (error) {
      console.error("Failed to toggle reward state:", error);
      alert("Failed to toggle reward state. Please try again.");
    } finally {
      setActionInProgress(false);
    }
  };

  if (loading) {
    return <div>Loading rewards...</div>;
  }

  return (
    <div>
      <h1 className="text-4xl font-extrabold text-purple-700 dark:text-purple-300 mb-6">
        Rewards Management
      </h1>
      <table className="table-auto w-full border-collapse border border-purple-300 rounded-lg shadow-md">
        <thead className="bg-purple-100 dark:bg-purple-800">
          <tr>
            <th className="border border-purple-300 px-4 py-2 text-left">Title</th>
            <th className="border border-purple-300 px-4 py-2 text-left">Cost</th>
            <th className="border border-purple-300 px-4 py-2 text-left">Type</th>
            <th className="border border-purple-300 px-4 py-2 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          {rewards.map((reward: Reward) => (
            <tr
              key={reward.id}
              className="hover:bg-purple-50 dark:hover:bg-purple-900 transition-colors"
            >
              <td className="border border-purple-300 px-4 py-2">{reward.name}</td>
              <td className="border border-purple-300 px-4 py-2">{reward.amount}</td>
              <td className="border border-purple-300 px-4 py-2">{getUserLabel(reward.type)}</td>
              <td className="border border-purple-300 px-4 py-2 flex items-center gap-4">
                <button
                  onClick={() => navigate(`/rewards/edit/${reward.id}`)}
                  className="text-purple-500 hover:text-purple-700"
                  disabled={actionInProgress}
                >
                  <FontAwesomeIcon icon={faEdit} size="lg" />
                </button>
                <button
                  onClick={() => toggleReward(reward.id, reward.active)}
                  className="text-green-500 hover:text-green-700"
                  disabled={actionInProgress}
                >
                  <FontAwesomeIcon icon={reward.active ? faToggleOn : faToggleOff} size="lg" />
                </button>
                <div className="ml-6">
                  <button
                    onClick={() => deleteReward(reward.id)}
                    className="text-red-500 hover:text-red-700"
                    disabled={actionInProgress}
                  >
                    <FontAwesomeIcon icon={faTrash} size="lg" />
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="flex justify-end mt-4">
        <button
          onClick={() => navigate("/rewards/add")}
          className={`px-3 py-2 border rounded ${
            actionInProgress || availableRewardTypes.length === 0
              ? "bg-purple-300 text-purple-500 cursor-not-allowed"
              : "bg-purple-100 text-purple-700 hover:bg-purple-200"
          }`}
          disabled={actionInProgress || availableRewardTypes.length === 0} // Disable if no available types
        >
          <FontAwesomeIcon icon={faPlus} />
        </button>
      </div>
    </div>
  );
};

export default Rewards;