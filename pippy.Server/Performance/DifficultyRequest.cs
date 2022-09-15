using Newtonsoft.Json;
using osu.Game.Beatmaps;
using osu.Game.Rulesets.Mods;
using osu.Game.Rulesets.Osu;
using osu.Game.Rulesets.Osu.Difficulty;
using osu.Game.Rulesets.Osu.Mods;

namespace pippy.Server.Performance {
    internal class DifficultyRequest : IRequest {
        public string Type { get; } = "difficulty";

        [JsonProperty("beatmap_path")]
        public readonly string BeatmapPath;

        [JsonProperty("mods")]
        [JsonConverter(typeof(ModListConverter))]
        public readonly Mod[] Mods;

        public DifficultyRequest(string beatmapPath, Mod[] mods) {
            BeatmapPath = beatmapPath;
            Mods = mods;
        }

        public IResponse GenerateResponse() {
            var beatmap = new FlatFileWorkingBeatmap(BeatmapPath);
            var calculator = new OsuDifficultyCalculator(new OsuRuleset().RulesetInfo, beatmap);
            var attributes = (OsuDifficultyAttributes) calculator.Calculate(Mods.Append(new OsuModClassic()));
            return new DifficultyResponse(attributes);
        }
    }
}
