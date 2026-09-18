"""The one-method fix that makes left-padded batched generation work on Ouro-1.4B BASE.

ByteDance shipped it themselves in Ouro-1.4B-Thinking's modeling_ouro.py (lines 198-219 of
that file) but not in Ouro-1.4B's. Their own docstring, quoted verbatim:

    The inherited ``Cache.get_mask_sizes`` falls back to ``(cache_position.shape[0], 0)``
    when ``layer_idx >= len(self.layers)``.  Because ``UniversalTransformerCache`` manages
    its own flat ``key_cache`` / ``value_cache`` lists and keeps ``self.layers`` empty, the
    fallback always fires.  During the prefill step this happens to be correct
    (``cache_position`` spans the full input), but during autoregressive decoding
    ``cache_position`` has length 1, so the mask is built for ``kv_length=1`` instead of
    ``cached_length + 1``.  As a result the 4D attention mask is too small and padding
    information is lost, corrupting batched generation for every sequence except the
    longest (unpadded) one.

We do NOT edit the cached file. We attach the identical method to the class object that the
dynamic module already loaded.
"""
import sys


def patch_universal_cache(model):
    """Attach Ouro-1.4B-Thinking's get_mask_sizes to whatever UniversalTransformerCache
    class this model's dynamic module defined. Returns (patched: bool, already: bool)."""
    mod = sys.modules[type(model).__module__]
    cls = getattr(mod, "UniversalTransformerCache")
    if "get_mask_sizes" in cls.__dict__:
        return False, True

    def get_mask_sizes(self, cache_position, layer_idx: int = 0):
        query_length = cache_position.shape[0]
        seq_length = self.get_seq_length(layer_idx)
        return seq_length + query_length, 0

    cls.get_mask_sizes = get_mask_sizes
    return True, False
