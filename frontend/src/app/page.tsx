import { sfetch } from "./lib/server";
import ProductCard, { type Product } from "./components/ProductCard";

type ProductListResponse = {
  items: Product[];
  total?: number;
};

export default async function CatalogPage() {
  const data = await sfetch<ProductListResponse>("/products?size=24"); // Flask: /api/products
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4">
      {data.items.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
