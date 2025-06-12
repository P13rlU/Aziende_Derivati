// src/components/DataTable.tsx
interface DataTableProps<T> {
    data: T[];
    columns: Array<{ key: keyof T; label: string }>;
    title?: string;
}

const DataTable = <T extends Record<string, any>>({ data, columns, title }: DataTableProps<T>) => {
    if (!data.length) {
        return <p>Nessun dato disponibile.</p>;
    }

    return (
        <div>
            {title && <h2>{title}</h2>}
            <table>
                <thead>
                <tr>
                    {columns.map(col => <th key={col.key as string}>{col.label}</th>)}
                </tr>
                </thead>
                <tbody>
                {data.map((item, idx) => (
                    <tr key={idx}>
                        {columns.map(col => (
                            <td key={col.key as string}>{item[col.key]}</td>
                        ))}
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
};

export default DataTable;