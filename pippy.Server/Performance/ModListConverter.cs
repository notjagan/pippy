using Newtonsoft.Json;
using osu.Game.Rulesets.Mods;
using osu.Game.Rulesets.Osu;

namespace pippy.Server.Performance {
    internal class ModListConverter : JsonConverter {
        public override bool CanConvert(Type objectType) {
            return objectType == typeof(Mod);
        }

        public override bool CanWrite => false;

        public override bool CanRead => true;

        public override object? ReadJson(JsonReader reader, Type objectType, object? existingValue, JsonSerializer serializer) {
            var acronyms = serializer.Deserialize<List<string>>(reader);
            var ruleset = new OsuRuleset();
            return acronyms?.Select(acroynm => ruleset.CreateModFromAcronym(acroynm))?.ToArray();
        }

        public override void WriteJson(JsonWriter writer, object? value, JsonSerializer serializer) {
            throw new NotImplementedException();
        }
    }
}
