using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;
using System.Reflection;

namespace pippy.Server {
    public class OverrideContractResolver : DefaultContractResolver {
        private readonly IDictionary<MemberInfo, JsonProperty> Overrides;

        public OverrideContractResolver(IDictionary<MemberInfo, JsonProperty> overrides) : base() {
            this.Overrides = overrides;
        }

        protected override JsonProperty CreateProperty(MemberInfo member, MemberSerialization memberSerialization) {
            var property = base.CreateProperty(member, memberSerialization);
            if (Overrides.TryGetValue(member, out JsonProperty? propertyOverride)) {
                if (propertyOverride.PropertyName != null) {
                    property.PropertyName = ResolvePropertyName(propertyOverride.PropertyName);
                }
                property.Ignored = propertyOverride.Ignored;
            }
            return property;
        }
    }
}
