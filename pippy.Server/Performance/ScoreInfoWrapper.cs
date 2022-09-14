using Newtonsoft.Json;
using osu.Game.Rulesets.Mods;
using osu.Game.Rulesets.Osu.Mods;
using osu.Game.Rulesets.Scoring;
using osu.Game.Scoring;

namespace pippy.Server.Performance {
    internal class ScoreInfoWrapper {
        [JsonProperty("count_300")]
        public readonly int Count300;

        [JsonProperty("count_100")]
        public readonly int Count100;

        [JsonProperty("count_50")]
        public readonly int Count50;

        [JsonProperty("count_miss")]
        public readonly int CountMiss;

        [JsonProperty("max_combo")]
        public readonly int MaxCombo;

        [JsonProperty("mods")]
        [JsonConverter(typeof(ModListConverter))]
        public readonly Mod[] Mods;

        public double Accuracy {
            get {
                var total = Count300 + Count100 + Count50 + CountMiss;
                return (double) ((6 * Count300) + (2 * Count100) + Count50) / (6 * total);
            }
        }

        public ScoreInfo ScoreInfo {
            get {
                return new ScoreInfo {
                    Accuracy = Accuracy,
                    MaxCombo = MaxCombo,
                    Statistics = new Dictionary<HitResult, int> {
                        { HitResult.Great, Count300 },
                        { HitResult.Ok, Count100 },
                        { HitResult.Meh, Count50 },
                        { HitResult.Miss, CountMiss }
                    },
                    Mods = Mods.Append(new OsuModClassic()).ToArray()
                };
            }
        }

        public ScoreInfoWrapper(int count300, int count100, int count50, int countMiss, int maxCombo, Mod[] mods) {
            Count300 = count300;
            Count100 = count100;
            Count50 = count50;
            CountMiss = countMiss;
            MaxCombo = maxCombo;
            Mods = mods;
        }
    }
}
