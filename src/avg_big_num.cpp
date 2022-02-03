#if defined(MYSQL_SERVER)
#include <m_string.h> /* To get stpcpy() */
#else
/* when compiled as standalone */
#include <string.h>
#endif

#include <ctype.h>
#include <gmp.h>
#include <mysql.h>

#include <cstring>
#include <string>

// C_MODE_START;
extern "C"
{
    bool big_average_init(UDF_INIT *initid, UDF_ARGS *args, char *message);
    void big_average_deinit(UDF_INIT *initid);
    void big_average_reset(UDF_INIT *initid, UDF_ARGS *args, char *is_null, char *message);
    void big_average_clear(UDF_INIT *initid, char *is_null, char *message);
    void big_average_add(UDF_INIT *initid, UDF_ARGS *args, char *is_null, char *message);
    char *big_average(UDF_INIT *initid, UDF_ARGS *args, char *result, unsigned long *length, char *is_null, char *error);
}
// C_MODE_END;

struct big_average_data
{
    mpz_t total;
};

bool big_average_init(UDF_INIT *initid, UDF_ARGS *args, char *message)
{
    struct big_average_data *data;

    if (args->arg_count != 1)
    {
        strcpy(message, "wrong number of arguments: big_average() requires a column name as arguments");
        return 1;
    }

    if (!(data = new (std::nothrow) big_average_data))
    {
        stpcpy(message, "Couldn't allocate memory");
        return 1;
    }

    mpz_init(data->total);
    
    mpz_set_ui(data->total, 0);

    initid->ptr = (char *)data;
    return 0;
}

void big_average_deinit(UDF_INIT *initid)
{
    void *void_ptr = initid->ptr;
    big_average_data *data = static_cast<big_average_data *>(void_ptr);
    mpz_clear(data->total);
    delete data;
}

/* This is only for MySQL 4.0 compability */
void big_average_reset(UDF_INIT *initid, UDF_ARGS *args, char *is_null, char *message)
{
    big_average_clear(initid, is_null, message);
    big_average_add(initid, args, is_null, message);
}

/* This is needed to get things to work in MySQL 4.1.1 and above */
void big_average_clear(UDF_INIT *initid, char *is_null,
                        char *message)
{
    struct big_average_data *data = (struct big_average_data *)initid->ptr;
}

void big_average_add(UDF_INIT *initid, UDF_ARGS *args,
                      char *is_null,
                      char *message)
{
    if (args->args[0] && args->args[0])
    {
        struct big_average_data *data = (struct big_average_data *)initid->ptr;

        mpz_t a;
        mpz_init(a);
        const char *as = (const char *)args->args[0];
        mpz_set_str(a, as, 16);
        mpz_add(data->total, data->total, a);
        mpz_clear(a);
    }
}

char *big_average(UDF_INIT *initid, UDF_ARGS *args, char *result, unsigned long *length, char *is_null, char *error)
{
    struct big_average_data *data = (struct big_average_data *)initid->ptr;
    *is_null = 0;
    // convert total to hex string
    mpz_get_str(result, 16, data->total);
    *length = strlen(result);
    return result;
}
