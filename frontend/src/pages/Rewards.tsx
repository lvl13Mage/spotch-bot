import { useState } from "react";
import axios from "axios";

const Rewards = () => {
  const [rewards, setRewards] = useState([]);
  const [name, setName] = useState("");

  const fetchRewards = async () => {
    const response = await axios.get("/api/rewards");
    setRewards(response.data);
  };

  const createReward = async () => {
    await axios.post("/api/rewards", { name });
    fetchRewards();
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Rewards</h1>
      <div className="mb-4">
        <input
          type="text"
          placeholder="Reward Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="border p-2 mr-2"
        />
        <button onClick={createReward} className="bg-blue-500 text-white px-4 py-2">
          Add Reward
        </button>
      </div>
      <ul>
        {rewards.map((reward: any) => (
          <li key={reward.id}>{reward.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default Rewards;