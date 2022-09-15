using Newtonsoft.Json;
using osu.Game.Beatmaps;
using osu.Game.Rulesets.Objects.Types;
using osu.Game.Rulesets.Objects.Legacy.Osu;
using osu.Game.Rulesets.Osu;
using osu.Game.Rulesets.Osu.Objects;

namespace pippy.Server.Beatmap {
    internal class MaxComboRequest : IRequest
    {
        public string Type { get; } = "max_combo";

        [JsonProperty("beatmap_path")]
        public readonly string BeatmapPath;

        public MaxComboRequest(string beatmapPath)
        {
            BeatmapPath = beatmapPath;
        }

        public IResponse GenerateResponse()
        {
            var beatmap = new FlatFileWorkingBeatmap(BeatmapPath).GetPlayableBeatmap(new OsuRuleset().RulesetInfo);
            var combo = beatmap.HitObjects.Count + beatmap.HitObjects.OfType<Slider>().Sum(slider => slider.NestedHitObjects.Count - 1);
            return new MaxComboResponse(combo);
        }
    }
}
