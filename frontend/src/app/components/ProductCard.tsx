"use client";

import Image from "next/image";

export type Product = {
  id: string | number;
  name: string;
  price: number;          // adjust if your API sends string -> change to `string` and cast
  images?: string[];
};

export default function ProductCard({ product }: { product: Product }) {
  const price = Number(product.price); // safe if price is already number
  const img = product.images?.[0];

  return (
    <div className="rounded-2xl shadow p-4 bg-white">
      <div className="relative w-full h-40">
        {img ? (
          <Image
            src={img}
            alt={product.name}
            fill
            className="object-cover rounded-xl"
            sizes="(max-width: 768px) 100vw, 25vw"
            priority={false}
          />
        ) : (
          <div className="w-full h-full rounded-xl bg-gray-100 grid place-items-center text-xs text-gray-500">
            No image
          </div>
        )}
      </div>

      <div className="mt-2 font-medium">{product.name}</div>
      <div className="text-sm">${price.toFixed(2)}</div>

      <button
        type="button"
        className="mt-3 w-full rounded-2xl bg-black text-white py-2"
        aria-label={`Add ${product.name} to cart`}
      >
        Add to cart
      </button>
    </div>
  );
}
